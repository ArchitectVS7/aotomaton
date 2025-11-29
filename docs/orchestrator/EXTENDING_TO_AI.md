# Extending to AI Agents

**Current State**: Human-in-the-loop MVP
**Future State**: Autonomous AI agents
**Migration Time**: 4-8 hours

---

## Current Architecture

The Thursian MVP uses **human agents** reading markdown guidelines:

1. Orchestrator creates task file (`.thursian/tasks/{task_id}.md`)
2. Human reads agent guidelines (`docs/agents/CODING_AGENT.md`)
3. Human completes task and creates output file
4. Orchestrator polls for completion
5. Human validator reviews and approves

**Benefits**:
- Validates workflow logic without AI costs
- Proves file protocol works
- Tests decision logging
- Human expertise for complex tasks

---

## Migration Path to AI Agents

### Phase 1: Add LLM Configuration (2 hours)

#### 1. Install Dependencies

```bash
pip install langchain-anthropic langchain-core
```

Update `requirements.txt`:
```
langgraph==0.2.28
typing-extensions==4.12.2
python-dotenv==1.0.1
langchain-anthropic==0.3.0
langchain-core==0.3.0
```

#### 2. Configure API Access

Create `.env` file:
```
ANTHROPIC_API_KEY=your-api-key-here
USE_AI_AGENTS=false  # Toggle between human/AI
```

#### 3. Create LLM Client

Create `orchestrator/llm_client.py`:
```python
"""LLM client for AI agents."""

import os
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()


class LLMClient:
    """Client for invoking LLM-powered agents."""

    def __init__(self):
        self.haiku = ChatAnthropic(
            model="claude-3-5-haiku-20241022",
            temperature=0.7,
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )

        self.sonnet = ChatAnthropic(
            model="claude-sonnet-4-5-20250929",
            temperature=0.5,
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )

    async def invoke_agent(
        self,
        agent_prompt: str,
        task_description: str,
        use_sonnet: bool = False
    ) -> str:
        """
        Invoke AI agent with task.

        Args:
            agent_prompt: System prompt (from agent guidelines)
            task_description: User task to complete
            use_sonnet: Use Sonnet instead of Haiku (for complex tasks)

        Returns:
            Agent's response (solution)
        """
        llm = self.sonnet if use_sonnet else self.haiku

        messages = [
            SystemMessage(content=agent_prompt),
            HumanMessage(content=task_description)
        ]

        response = await llm.ainvoke(messages)
        return response.content


# Singleton instance
llm_client = LLMClient()
```

---

### Phase 2: Convert Guidelines to System Prompts (1 hour)

Create `orchestrator/agent_prompts.py`:
```python
"""System prompts for AI agents."""

import os

from .state import AgentRole


def load_agent_prompt(agent_role: AgentRole) -> str:
    """
    Load agent guidelines and convert to system prompt.

    Args:
        agent_role: Agent role to load

    Returns:
        System prompt for the agent
    """
    if agent_role == AgentRole.CODING_AGENT:
        # Read from markdown file
        with open("docs/agents/CODING_AGENT.md", 'r') as f:
            guidelines = f.read()

        return f"""You are a Coding Agent in the Thursian development orchestrator.

{guidelines}

IMPORTANT:
- Your output will be written directly to the output file
- Include "**Status: COMPLETE**" at the end
- Format as markdown
- Be thorough but concise
"""

    elif agent_role == AgentRole.REVIEW_AGENT:
        with open("docs/agents/REVIEW_AGENT.md", 'r') as f:
            guidelines = f.read()

        return f"""You are a Review Agent in the Thursian development orchestrator.

{guidelines}

IMPORTANT:
- Your validation will be written directly to the validation file
- Mark status as "**Status: APPROVED**" or "**Status: NEEDS_REVISION**"
- Be constructive and specific
- Format as markdown
"""

    raise ValueError(f"Unknown agent role: {agent_role}")
```

---

### Phase 3: Implement AI Nodes (3 hours)

Create `orchestrator/nodes_ai.py`:
```python
"""AI-powered node implementations."""

from typing import Dict, Any
import logging

from .state import ThursianState, WorkflowPhase
from .helpers import transition_phase, add_decision_log, add_error, write_decision_log_to_file
from .llm_client import llm_client
from .agent_prompts import load_agent_prompt

logger = logging.getLogger(__name__)


async def execution_node_ai(state: ThursianState) -> Dict[str, Any]:
    """
    AI-powered execution node.

    Instead of waiting for human, invokes AI agent to complete task.
    """
    logger.info(f"AI execution for task {state['current_task_id']}")

    try:
        task_description = state['task_description']
        agent_prompt = load_agent_prompt(state['primary_agent'])

        # Invoke AI agent
        logger.info("Invoking AI coding agent...")
        response = await llm_client.invoke_agent(
            agent_prompt=agent_prompt,
            task_description=task_description,
            use_sonnet=False  # Use Haiku for speed
        )

        # Write output directly
        output_file_path = os.path.join(
            state['thursian_dir'],
            'output',
            f'{state["current_task_id"]}_output.md'
        )

        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

        with open(output_file_path, 'w') as f:
            f.write(response)

        logger.info(f"AI agent completed task: {output_file_path}")

        result = {
            **transition_phase(state, WorkflowPhase.EXECUTION),
            **add_decision_log(
                state,
                reasoning="AI agent completed task implementation",
                outcome=f"Output generated at {output_file_path}",
                agent_assigned=state['primary_agent'].value,
                doc_reference="docs/agents/CODING_AGENT.md",
                tool_used="ai_llm_invocation"
            ),
            'output_file_path': output_file_path,
            'waiting_for_human': False  # No longer waiting!
        }

        write_decision_log_to_file({**state, **result})

        return result

    except Exception as e:
        logger.error(f"AI execution failed: {e}")
        return add_error(state, f"AI execution failed: {str(e)}")


async def validation_node_ai(state: ThursianState) -> Dict[str, Any]:
    """
    AI-powered validation node.

    Instead of waiting for human, invokes AI agent to validate.
    """
    logger.info(f"AI validation for task {state['current_task_id']}")

    try:
        # Read primary output
        with open(state['output_file_path'], 'r') as f:
            primary_output = f.read()

        agent_prompt = load_agent_prompt(state['validator_agent'])

        # Build validation request
        validation_request = f"""Review the following output:

{primary_output}

Provide your validation according to the guidelines."""

        # Invoke AI validator
        logger.info("Invoking AI review agent...")
        response = await llm_client.invoke_agent(
            agent_prompt=agent_prompt,
            task_description=validation_request,
            use_sonnet=True  # Use Sonnet for better analysis
        )

        # Write validation
        validation_file_path = os.path.join(
            state['thursian_dir'],
            'output',
            f'{state["current_task_id"]}_validation.md'
        )

        with open(validation_file_path, 'w') as f:
            f.write(response)

        logger.info(f"AI validator completed: {validation_file_path}")

        result = {
            **add_decision_log(
                state,
                reasoning="AI agent completed validation review",
                outcome=f"Validation generated at {validation_file_path}",
                agent_assigned=state['validator_agent'].value,
                doc_reference="docs/agents/REVIEW_AGENT.md",
                tool_used="ai_llm_invocation"
            ),
            'validation_file_path': validation_file_path,
            'waiting_for_human': False  # No longer waiting!
        }

        write_decision_log_to_file({**state, **result})

        return result

    except Exception as e:
        logger.error(f"AI validation failed: {e}")
        return add_error(state, f"AI validation failed: {str(e)}")
```

---

### Phase 4: Toggle Mode (1 hour)

Update `orchestrator/graph.py`:
```python
"""LangGraph workflow graph construction with AI/Human toggle."""

import os
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv

from .state import ThursianState
from .nodes import (
    task_selection_node,
    assignment_node,
    execution_node,
    validation_node,
    completion_node
)
from .nodes_ai import execution_node_ai, validation_node_ai
from .routing import route_after_execution, route_after_validation

load_dotenv()


def create_thursian_workflow() -> StateGraph:
    """Create workflow with AI/Human toggle."""

    # Check if AI agents enabled
    use_ai = os.getenv("USE_AI_AGENTS", "false").lower() == "true"

    workflow = StateGraph(ThursianState)

    # Add nodes (conditionally choose AI or human)
    workflow.add_node("task_selection", task_selection_node)
    workflow.add_node("assignment", assignment_node)
    workflow.add_node(
        "execution_node",
        execution_node_ai if use_ai else execution_node
    )
    workflow.add_node(
        "validation_node",
        validation_node_ai if use_ai else validation_node
    )
    workflow.add_node("completion", completion_node)

    # Rest of graph construction...
    # (same as before)
```

---

## Testing Strategy

### 1. Validate with Humans First

Before enabling AI:
```bash
USE_AI_AGENTS=false python -m orchestrator.main
```

Complete workflow manually to prove logic works.

### 2. Test AI with Same Tasks

Enable AI and run same tasks:
```bash
USE_AI_AGENTS=true python -m orchestrator.main
```

### 3. Compare Outputs

Compare human vs AI outputs:
- Correctness
- Completeness
- Quality
- Decision logs

### 4. Gradual Rollout

- Week 1: Human validation
- Week 2: AI execution + human validation
- Week 3: Full AI with human oversight
- Week 4+: Autonomous AI

---

## Cost Monitoring

Track LLM costs in decision logs:
```python
def add_decision_log(...):
    log_entry: DecisionLog = {
        # ... existing fields
        'llm_tokens_used': response.usage.total_tokens,
        'llm_cost_usd': calculate_cost(response.usage),
        'llm_model': response.model
    }
```

---

## Best Practices

1. **Start with Haiku** - Faster and cheaper for most tasks
2. **Use Sonnet for validation** - Better analysis and edge case detection
3. **Keep human override** - Toggle back to human for complex tasks
4. **Monitor quality** - Track approval rates
5. **Iterative prompts** - Refine agent prompts based on results

---

## Expected Benefits

**Speed**: Tasks complete in seconds instead of minutes
**Consistency**: Same quality every time
**Scalability**: Handle multiple tasks in parallel
**Cost**: ~$0.01-0.10 per task (vs. human time)

---

## Rollback Plan

If AI quality is insufficient:
```bash
USE_AI_AGENTS=false
```

Instantly revert to human agents while debugging.

---

**Migration Time**: 4-8 hours total
**Compatibility**: 100% backward compatible
**Risk**: Low (toggle-based, can revert instantly)
