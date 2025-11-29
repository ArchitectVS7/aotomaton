# LangGraph Patterns from Focus-Pocus

**Source**: Focus-Pocus `api/graph/` implementation
**Purpose**: Architectural patterns for building the Automaton orchestrator
**Last Updated**: 2025-01-29

---

## Overview

Focus-Pocus uses LangGraph to orchestrate a 9-phase focus group workflow with human-in-the-loop gates. These patterns are proven in production and can be adapted for the Automaton development orchestrator.

---

## 1. State Definition Pattern

### Core Pattern: TypedDict with Annotated Accumulation

```python
from typing import TypedDict, Annotated, List, Optional, Dict, Any
from datetime import datetime
import operator

class SimpleFocusGroupState(TypedDict):
    # Metadata
    project_id: str
    thread_id: str
    user_id: str
    created_at: datetime

    # Configuration
    enabled_gates: List[HumanGate]
    turbo_mode: bool

    # Current state
    current_phase: ProjectPhase
    phase_history: Annotated[List[ProjectPhase], operator.add]  # Accumulates!

    # Data that accumulates across nodes
    personas: Annotated[List[Persona], operator.add]
    messages: Annotated[List[Dict[str, Any]], operator.add]
    errors: Annotated[List[str], operator.add]

    # Data that gets replaced
    approved_personas: List[Persona]
    waiting_for_human: bool
```

### Key Insights

**✅ Use `Annotated[List[T], operator.add]` for accumulating data**
- Lists with `operator.add` APPEND new items instead of replacing
- Perfect for building up context across workflow steps
- Examples: phase history, logs, errors, artifacts

**✅ Use plain `List[T]` for replacement data**
- When you want to completely replace a list, don't use `operator.add`
- Examples: current approved items, active blockers

**✅ Define Phase Enums for type safety**

```python
from enum import Enum

class ProjectPhase(str, Enum):
    INITIALIZATION = "initialization"
    IDEA_CLARIFICATION = "idea_clarification"
    PERSONA_GENERATION = "persona_generation"
    PERSONA_APPROVAL = "persona_approval"        # Gate
    FOCUS_GROUP_ROUND = "focus_group_round"
    SYNTHESIS = "synthesis"
    REPORT_GENERATION = "report_generation"
    FINAL_REVIEW = "final_review"                # Gate
    COMPLETED = "completed"
```

**For Automaton orchestrator, use:**

```python
class WorkflowPhase(str, Enum):
    IDLE = "idle"
    TASK_SELECTION = "task_selection"
    PLANNING = "planning"
    ASSIGNMENT = "assignment"
    EXECUTION = "execution"
    SELF_CHECK = "self_check"
    SECOND_CHECK = "second_check"
    APPROVAL_LOOP = "approval_loop"
    ESCALATION = "escalation"
    DOCUMENTATION = "documentation"
    COMPLETED = "completed"
```

---

## 2. Helper Functions Pattern

### State Transition Helpers

**Pattern**: Create helper functions to ensure consistent state updates

```python
def transition_phase(state: SimpleFocusGroupState, new_phase: ProjectPhase) -> Dict[str, Any]:
    """Helper to transition to a new phase and update phase history."""
    return {
        'current_phase': new_phase,
        'phase_history': [new_phase]  # operator.add appends this
    }

def add_error(state: SimpleFocusGroupState, error_message: str) -> Dict[str, Any]:
    """Add timestamped error to state."""
    return {
        'errors': [f"{datetime.utcnow().isoformat()} - {error_message}"]
    }

def should_skip_gate(state: SimpleFocusGroupState, gate: HumanGate) -> bool:
    """Check if gate should be skipped (turbo mode or gate not enabled)."""
    if state.get('turbo_mode', False):
        return True
    enabled_gates = state.get('enabled_gates', [])
    if gate not in enabled_gates:
        return True
    return False
```

**For Automaton, create:**
- `transition_phase()` - Phase transitions with history tracking
- `add_log()` - Timestamped logging
- `add_blocker()` - Track workflow blockers
- `create_task_file()` - Generate .thursian/ task files
- `detect_completion()` - Check for output files

---

## 3. Node Implementation Pattern

### Standard Node Structure

**Every node follows this pattern:**

```python
async def node_name(state: SimpleFocusGroupState) -> Dict[str, Any]:
    """
    Node description.

    Args:
        state: Current workflow state

    Returns:
        Dictionary of state updates (merged automatically by LangGraph)
    """
    logger.info(f"Starting node for project {state['project_id']}")

    try:
        # 1. Extract relevant state
        raw_idea = state['raw_idea']
        questions = state.get('clarification_questions', [])

        # 2. Process (LLM call, calculation, file I/O, etc.)
        system_prompt = """You are a helpful assistant..."""
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"User input: {raw_idea}")
        ]
        response = haiku_llm.invoke(messages)

        # 3. Parse/validate response
        try:
            if '```json' in response.content:
                json_text = response.content.split('```json')[1].split('```')[0].strip()
            result = json.loads(json_text)
        except Exception as parse_error:
            logger.warning(f"Parse error: {parse_error}")
            result = fallback_value

        # 4. Return state update dict
        return {
            **transition_phase(state, ProjectPhase.NEXT_PHASE),
            'field_name': result,
            'messages': [{'role': 'assistant', 'content': response.content}],
            'waiting_for_human': False
        }

    except Exception as e:
        logger.error(f"Error in node: {e}")
        return add_error(state, f"Node failed: {str(e)}")
```

### Key Node Rules

✅ **All nodes are async-compatible** (even if not using `await`)
✅ **Return dictionaries, not state objects** (LangGraph merges automatically)
✅ **Use spread operator** (`**transition_phase()`) to preserve existing state
✅ **Always include error handling** with try/except
✅ **Transition phase explicitly** in return statement
✅ **Log key operations** for debugging
✅ **Return partial updates** - only include changed fields

### Example Node: Task File Creation

**For Automaton orchestrator:**

```python
def create_task_file_node(state: DevWorkflowState) -> Dict[str, Any]:
    """Create task definition file in .thursian/ directory."""
    logger.info(f"Creating task file for {state['current_task_id']}")

    try:
        task_id = state['current_task_id']
        task_desc = state['task_description']

        # Generate markdown task file
        task_content = f"""# TASK: {task_desc}

**ID**: {task_id}
**Status**: PENDING
**Created**: {datetime.now().isoformat()}

## Role Assignment
**Primary Agent**: {state['primary_agent'].value}
**Validator Agent**: {state['validator_agent'].value}

## Context
{state.get('task_context', 'No additional context')}

## Expected Output
Write results to .thursian/output/{task_id}_output.md
"""

        # Write to file
        task_file_path = os.path.join(
            state['thursian_dir'],
            'tasks',
            f'{task_id}.md'
        )

        with open(task_file_path, 'w') as f:
            f.write(task_content)

        return {
            **transition_phase(state, WorkflowPhase.EXECUTION),
            'task_file_path': task_file_path,
            'logs': [f"{datetime.now()}: Created task file {task_file_path}"]
        }

    except Exception as e:
        logger.error(f"Error creating task file: {e}")
        return add_error(state, f"Task file creation failed: {str(e)}")
```

---

## 4. Conditional Routing Pattern

### Routing Function Structure

**Pattern**: Use routing functions to determine next node based on state

```python
from typing import Literal

def route_after_clarification(
    state: SimpleFocusGroupState
) -> Literal["generate_vision_statement", "clarify_idea"]:
    """Route after idea clarification."""

    # In turbo mode, always proceed
    if state.get('turbo_mode'):
        return "generate_vision_statement"

    # If we have answers OR not waiting for human, proceed
    if state.get('clarification_answers') is not None or not state.get('waiting_for_human', False):
        return "generate_vision_statement"

    # Otherwise stay at clarification (waiting for user input)
    return "clarify_idea"  # Loops back to same node

def route_after_personas(
    state: SimpleFocusGroupState
) -> Literal["persona_approval_gate", "focus_group_moderator", END]:
    """Route after persona generation."""

    if state.get('errors'):
        return END  # Stop on errors

    # Check if we need approval gate
    if state.get('current_phase') == ProjectPhase.PERSONA_APPROVAL:
        return "persona_approval_gate"

    # Otherwise skip to focus group (turbo mode)
    return "focus_group_moderator"
```

### Routing Patterns

**✅ Loop-back pattern** - Return to same node when waiting:
```python
if state.get('waiting_for_human'):
    return "same_node"  # Stays in current node
```

**✅ Conditional branching** - Different paths based on state:
```python
if state.get('turbo_mode'):
    return "skip_gate"
else:
    return "approval_gate"
```

**✅ Early termination** - Stop on errors:
```python
if state.get('errors'):
    return END
```

**For Automaton, create routing like:**

```python
def route_after_execution(
    state: DevWorkflowState
) -> Literal["second_check", "execution"]:
    """Route after primary agent execution."""

    # Check if output file exists
    task_id = state['current_task_id']
    output_file = f"{state['thursian_dir']}/output/{task_id}_output.md"

    if not os.path.exists(output_file):
        return "execution"  # Loop back, keep waiting

    # Check status
    status_file = f"{state['thursian_dir']}/status.txt"
    with open(status_file, 'r') as f:
        status = f.read().strip()

    if status != "COMPLETE":
        return "execution"  # Loop back

    return "second_check"  # Proceed to validation
```

---

## 5. Graph Construction Pattern

### Building the State Machine

```python
from langgraph.graph import StateGraph, END

def create_workflow_graph(checkpointer=None) -> StateGraph:
    """Create and compile the workflow graph."""

    workflow = StateGraph(SimpleFocusGroupState)

    # 1. Add all nodes
    workflow.add_node("initialize_project", initialize_project)
    workflow.add_node("clarify_idea", clarify_idea)
    workflow.add_node("generate_personas", generate_personas)
    workflow.add_node("persona_approval_gate", persona_approval_gate)
    workflow.add_node("focus_group_moderator", focus_group_moderator)

    # 2. Set entry point
    workflow.set_entry_point("initialize_project")

    # 3. Add simple edges (deterministic flow)
    workflow.add_edge("initialize_project", "clarify_idea")

    # 4. Add conditional edges (routing logic)
    workflow.add_conditional_edges(
        "clarify_idea",
        route_after_clarification,
        {
            "generate_vision_statement": "generate_vision_statement",
            "clarify_idea": "clarify_idea"  # Loop back
        }
    )

    workflow.add_conditional_edges(
        "generate_personas",
        route_after_personas,
        {
            "persona_approval_gate": "persona_approval_gate",
            "focus_group_moderator": "focus_group_moderator",
            END: END  # Terminate on errors
        }
    )

    # 5. Compile with optional checkpointer
    return workflow.compile(checkpointer=checkpointer)
```

### Graph Construction Rules

✅ **Add all nodes first** before defining edges
✅ **Set entry point explicitly**
✅ **Use simple edges** for deterministic A→B transitions
✅ **Use conditional edges** when routing depends on state
✅ **Map all routing outcomes** in the dictionary
✅ **Compile last** with optional checkpointer

**For Automaton:**

```python
def create_dev_workflow() -> StateGraph:
    workflow = StateGraph(DevWorkflowState)

    # Nodes
    workflow.add_node("task_selection", select_next_task)
    workflow.add_node("assignment", assign_agents)
    workflow.add_node("create_task_file", create_task_file_node)
    workflow.add_node("execution_wait", wait_for_completion)
    workflow.add_node("validation", validator_review)
    workflow.add_node("approval", check_approval)

    # Entry
    workflow.set_entry_point("task_selection")

    # Simple edges
    workflow.add_edge("task_selection", "assignment")
    workflow.add_edge("assignment", "create_task_file")

    # Conditional edges
    workflow.add_conditional_edges(
        "execution_wait",
        route_after_execution,
        {
            "second_check": "validation",
            "execution": "execution_wait"  # Loop
        }
    )

    return workflow.compile()
```

---

## 6. Human-in-the-Loop Gate Pattern

### Gate Implementation

**Pattern**: Gates pause workflow for human input

```python
def persona_approval_gate(state: SimpleFocusGroupState) -> Dict[str, Any]:
    """Wait for human approval of personas."""
    logger.info(f"Processing persona approval for project {state['project_id']}")

    try:
        # Get approved personas (set by user action via API)
        approved = state.get('approved_personas', [])

        if len(approved) < 3:
            return {
                'waiting_for_human': True,
                'current_gate': HumanGate.PERSONA_APPROVAL,
                'gate_data': {'message': 'Need at least 3 approved personas'}
            }

        logger.info(f"Approved {len(approved)} personas, proceeding")

        return {
            **transition_phase(state, ProjectPhase.FOCUS_GROUP_ROUND),
            'waiting_for_human': False,
            'current_gate': None,
            'gate_data': None
        }

    except Exception as e:
        logger.error(f"Error in persona approval gate: {e}")
        return add_error(state, f"Persona approval failed: {str(e)}")
```

### Gate Skip Logic

**Pattern**: Check if gate should be bypassed

```python
def generate_personas(state: SimpleFocusGroupState) -> Dict[str, Any]:
    # ... persona generation logic ...

    # Check if we should skip approval gate
    skip_gate = should_skip_gate(state, HumanGate.PERSONA_APPROVAL)

    if skip_gate:
        logger.info("Skipping persona approval gate (turbo mode)")
        return {
            **transition_phase(state, ProjectPhase.FOCUS_GROUP_ROUND),
            'personas': personas,
            'approved_personas': personas,  # Auto-approve
            'waiting_for_human': False
        }
    else:
        logger.info("Entering persona approval gate")
        return {
            **transition_phase(state, ProjectPhase.PERSONA_APPROVAL),
            'personas': personas,
            'waiting_for_human': True,
            'current_gate': HumanGate.PERSONA_APPROVAL.value,
            'gate_data': {'personas': personas}
        }
```

### Gate Features

✅ **Three-state flag system**:
- `waiting_for_human: bool` - Is workflow paused?
- `current_gate: str` - Which gate is blocking?
- `gate_data: dict` - Context for UI to render approval interface

✅ **Turbo mode bypass** - Can skip all gates
✅ **Selective gates** - `enabled_gates` list controls which gates are active
✅ **Loop-back routing** - Gates can keep workflow in same node until approval

**For Automaton gates:**

```python
class GateType(str, Enum):
    QUALITY_CHECK = "quality_check"
    APPROVAL_REQUIRED = "approval_required"
    ESCALATION = "escalation"

def quality_check_gate(state: DevWorkflowState) -> Dict[str, Any]:
    """Validator reviews primary agent's work."""

    # Check if validation completed
    validation_file = f"{state['thursian_dir']}/approvals/{state['current_task_id']}_review.md"

    if not os.path.exists(validation_file):
        return {
            'waiting_for_human': True,
            'current_gate': GateType.QUALITY_CHECK,
            'gate_data': {
                'task_id': state['current_task_id'],
                'validator': state['validator_agent'].value
            }
        }

    # Read validation result
    with open(validation_file, 'r') as f:
        result = f.read()

    if "APPROVED" in result:
        return {
            **transition_phase(state, WorkflowPhase.DOCUMENTATION),
            'waiting_for_human': False,
            'current_gate': None
        }
    else:
        # Rework required
        return {
            **transition_phase(state, WorkflowPhase.EXECUTION),
            'approval_iteration': state.get('approval_iteration', 0) + 1,
            'review_comments': [result]
        }
```

---

## 7. LLM Model Selection Pattern

### Tiered LLM Usage

**Pattern**: Use different models for different quality/speed needs

```python
# Fast, cost-effective for most operations
haiku_llm = ChatAnthropic(
    model="claude-3-5-haiku-20241022",
    temperature=0.7,
    max_tokens=4096
)

# High quality for final outputs
sonnet_llm = ChatAnthropic(
    model="claude-sonnet-4-5-20250929",
    temperature=0.5,
    max_tokens=8192
)

# Higher temperature for diversity (in persona generation)
persona_llm = ChatAnthropic(
    model="claude-3-5-haiku-20241022",
    temperature=0.8,  # Increased for variation
    max_tokens=4096
)
```

### Usage Guidelines

**Use Haiku for:**
- Parsing and classification
- Intermediate processing
- Data extraction
- Validation checks
- High-volume operations

**Use Sonnet for:**
- Final reports
- Complex reasoning
- Critical decisions
- User-facing content
- Quality-sensitive outputs

**For Automaton:**
- Use Haiku for task routing and validation
- Use Sonnet for escalation decisions and final summaries

---

## 8. API Invocation Pattern

### Starting and Continuing Workflows

```python
# Start workflow
workflow = get_workflow_graph(use_checkpointer=True)
config = {"configurable": {"thread_id": thread_id}}
result = await workflow.ainvoke(initial_state, config)

# Continue workflow with updates (e.g., after human input)
updates = {
    'approved_personas': user_selected_personas,
    'waiting_for_human': False
}
await workflow.aupdate_state(config, updates)
result = await workflow.ainvoke(None, config)  # None = use existing state
```

### Key Points

✅ **Thread ID** enables state persistence across calls
✅ **First call**: `ainvoke(initial_state, config)`
✅ **Continuation**: `ainvoke(None, config)` - uses stored state
✅ **State updates**: `aupdate_state()` merges changes before resuming
✅ **Config object**: `{"configurable": {"thread_id": ...}}`

**For Automaton API:**

```python
@app.post("/workflow/start")
async def start_workflow(req: StartWorkflowRequest):
    workflow_id = str(uuid.uuid4())

    initial_state = {
        "workflow_id": workflow_id,
        "project_id": req.project_id,
        "current_phase": WorkflowPhase.IDLE,
        # ... other initial state
    }

    workflow = create_dev_workflow()
    result = await workflow.ainvoke(initial_state)

    return {"workflow_id": workflow_id, "status": result['current_phase']}

@app.post("/workflow/{workflow_id}/continue")
async def continue_workflow(workflow_id: str):
    workflow = create_dev_workflow()
    config = {"configurable": {"thread_id": workflow_id}}

    # Continue from stored state
    result = await workflow.ainvoke(None, config)

    return {"phase": result['current_phase']}
```

---

## 9. Error Handling Strategy

### Error Accumulation Pattern

**Don't throw exceptions - accumulate errors in state**

```python
def some_node(state: State) -> Dict[str, Any]:
    try:
        # ... processing ...
        return {
            'field': result
        }
    except Exception as e:
        logger.error(f"Error in node: {e}")
        return {
            'errors': [f"{datetime.now().isoformat()}: {str(e)}"]
        }

# Then in routing:
def route_function(state: State) -> Literal["next", END]:
    if state.get('errors'):
        return END  # Terminate workflow on errors
    return "next"
```

### Graceful Degradation

**Provide fallback values instead of failing**

```python
try:
    json_result = json.loads(response.content)
except JSONDecodeError:
    logger.warning("JSON parse failed, using fallback")
    json_result = {
        "status": "unknown",
        "message": response.content[:200]  # Truncated raw response
    }
```

---

## 10. Persistence Pattern (PostgreSQL Checkpointer)

### Setup (Currently Disabled in Focus-Pocus for Testing)

```python
from langgraph.checkpoint.postgres import PostgresSaver
import psycopg

def get_postgres_checkpointer() -> PostgresSaver:
    """Create PostgreSQL checkpoint saver for workflow persistence."""
    db_url = os.getenv('DATABASE_URL')
    conn = psycopg.connect(db_url, autocommit=True)

    checkpointer = PostgresSaver(conn)
    checkpointer.setup()  # Creates checkpoint tables

    return checkpointer

def get_workflow_graph(use_checkpointer: bool = True):
    """Get compiled workflow graph (singleton pattern)."""
    global _compiled_graph

    if _compiled_graph is None:
        checkpointer = None
        if use_checkpointer:
            checkpointer = get_postgres_checkpointer()

        _compiled_graph = create_workflow_graph(checkpointer)

    return _compiled_graph
```

**For Automaton**: Enable checkpointing in Week 2 after basic workflow validated

---

## Summary: Key Patterns for Automaton

### 1. State Management
- ✅ Use `Annotated[List[T], operator.add]` for logs, errors, phase history
- ✅ Define clear phase enums
- ✅ Helper functions for state transitions

### 2. Node Implementation
- ✅ Async-compatible functions
- ✅ Return dictionaries (auto-merged)
- ✅ Try/except with error accumulation
- ✅ Explicit phase transitions

### 3. Routing
- ✅ Loop-back for waiting states
- ✅ Conditional branching on state flags
- ✅ Early termination on errors

### 4. Human-in-the-Loop
- ✅ Three-state flag system (waiting, gate type, gate data)
- ✅ Turbo mode bypass option
- ✅ Selective gate enablement

### 5. File Protocol Integration
- ✅ Node reads/writes .thursian/ files
- ✅ Polling for completion files
- ✅ Status file management

---

## Next Steps

1. **Implement basic state** with WorkflowPhase enum
2. **Create 3 core nodes**: task_selection, assignment, execution_wait
3. **Add file I/O helpers** for .thursian/ directory
4. **Build simple graph** with one conditional edge
5. **Test end-to-end** with a single task

**Start simple, then add complexity incrementally!**
