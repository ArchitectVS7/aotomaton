"""LangGraph workflow node implementations."""

from typing import Dict, Any
from datetime import datetime
import os
import logging

from .state import ThursianState, WorkflowPhase, AgentRole
from .helpers import (
    transition_phase,
    add_decision_log,
    add_error,
    write_decision_log_to_file,
    update_status_file
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def task_selection_node(state: ThursianState) -> Dict[str, Any]:
    """
    Select next task from task queue.

    Reads from .thursian/task_queue.txt and extracts first line as task.
    Generates unique task_id based on timestamp.
    """
    logger.info(f"Task selection for workflow {state['workflow_id']}")

    try:
        task_queue_file = os.path.join(state['thursian_dir'], 'task_queue.txt')

        if not os.path.exists(task_queue_file):
            return add_error(state, "Task queue file not found")

        with open(task_queue_file, 'r') as f:
            lines = f.readlines()

        if not lines:
            return add_error(state, "Task queue is empty")

        # Get first task
        task_description = lines[0].strip()

        # Generate task ID
        task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Update task queue (remove first line)
        with open(task_queue_file, 'w') as f:
            f.writelines(lines[1:])

        logger.info(f"Selected task: {task_id} - {task_description}")

        result = {
            **transition_phase(state, WorkflowPhase.ASSIGNMENT),
            **add_decision_log(
                state,
                reasoning="Selected first task from FIFO queue",
                outcome=f"Task selected: {task_description}",
                tool_used="file_read"
            ),
            'current_task_id': task_id,
            'task_description': task_description
        }

        # Write decision log to file
        write_decision_log_to_file({**state, **result})

        return result

    except Exception as e:
        logger.error(f"Error in task_selection_node: {e}")
        return add_error(state, f"Task selection failed: {str(e)}")


def assignment_node(state: ThursianState) -> Dict[str, Any]:
    """
    Assign agents to task.

    Assigns primary_agent (CODING_AGENT) and validator_agent (REVIEW_AGENT).
    Logs decision with reasoning.
    """
    logger.info(f"Assigning agents for task {state['current_task_id']}")

    try:
        # Simple deterministic assignment
        primary_agent = AgentRole.CODING_AGENT
        validator_agent = AgentRole.REVIEW_AGENT

        logger.info(f"Assigned: Primary={primary_agent.value}, Validator={validator_agent.value}")

        result = {
            **transition_phase(state, WorkflowPhase.EXECUTION),
            **add_decision_log(
                state,
                reasoning="Task requires code implementation, assigned coding agent with review validation",
                outcome=f"Primary: {primary_agent.value}, Validator: {validator_agent.value}",
                agent_assigned=primary_agent.value,
                doc_reference="docs/agents/CODING_AGENT.md",
                tool_used="agent_assignment"
            ),
            'primary_agent': primary_agent,
            'validator_agent': validator_agent
        }

        write_decision_log_to_file({**state, **result})

        return result

    except Exception as e:
        logger.error(f"Error in assignment_node: {e}")
        return add_error(state, f"Agent assignment failed: {str(e)}")


def execution_node(state: ThursianState) -> Dict[str, Any]:
    """
    Create task file for human agent to complete.

    Creates task definition in .thursian/tasks/{task_id}.md with full context.
    Sets waiting_for_human=True.
    Human reads docs/agents/CODING_AGENT.md and completes task.
    """
    logger.info(f"Execution node for task {state['current_task_id']}")

    try:
        task_id = state['current_task_id']
        task_description = state['task_description']

        # Create task file
        task_file_path = os.path.join(state['thursian_dir'], 'tasks', f'{task_id}.md')
        os.makedirs(os.path.dirname(task_file_path), exist_ok=True)

        task_content = f"""# Task: {task_id}

## Description

{task_description}

## Agent Assignment

**Primary Agent**: {state['primary_agent'].value}
**Agent Guidelines**: docs/agents/CODING_AGENT.md

## Instructions

1. Read the agent guidelines at `docs/agents/CODING_AGENT.md`
2. Implement the solution as described
3. Create output file at: `.thursian/output/{task_id}_output.md`
4. Include "**Status: COMPLETE**" in the output file

## Expected Output

File: `.thursian/output/{task_id}_output.md`

Format:
```markdown
# Task Output: {task_id}

## Implementation

[Your solution here]

## Notes

[Any relevant notes or considerations]

**Status: COMPLETE**
```

## Workflow Information

- Workflow ID: {state['workflow_id']}
- Created: {datetime.now().isoformat()}
"""

        with open(task_file_path, 'w') as f:
            f.write(task_content)

        # Set expected output file path
        output_file_path = os.path.join(state['thursian_dir'], 'output', f'{task_id}_output.md')

        logger.info(f"Created task file: {task_file_path}")
        print(f"\n{'='*60}")
        print(f"TASK READY: {task_id}")
        print(f"Task file: {task_file_path}")
        print(f"Agent guidelines: docs/agents/CODING_AGENT.md")
        print(f"Output file: {output_file_path}")
        print(f"{'='*60}\n")

        result = {
            **add_decision_log(
                state,
                reasoning=f"Created task file for human agent to complete",
                outcome=f"Waiting for human to complete task at {output_file_path}",
                agent_assigned=state['primary_agent'].value,
                doc_reference="docs/agents/CODING_AGENT.md",
                tool_used="file_creation"
            ),
            'task_file_path': task_file_path,
            'output_file_path': output_file_path,
            'waiting_for_human': True
        }

        write_decision_log_to_file({**state, **result})
        update_status_file({**state, **result})

        return result

    except Exception as e:
        logger.error(f"Error in execution_node: {e}")
        return add_error(state, f"Execution node failed: {str(e)}")


def validation_node(state: ThursianState) -> Dict[str, Any]:
    """
    Create validation task for review agent.

    Creates validation task in .thursian/tasks/{task_id}_validation.md.
    Sets waiting_for_human=True.
    Human reads docs/agents/REVIEW_AGENT.md and validates output.
    """
    logger.info(f"Validation node for task {state['current_task_id']}")

    try:
        task_id = state['current_task_id']

        # Create validation task file
        validation_task_file = os.path.join(
            state['thursian_dir'],
            'tasks',
            f'{task_id}_validation.md'
        )

        validation_content = f"""# Validation Task: {task_id}

## Primary Output to Review

File: `.thursian/output/{task_id}_output.md`

## Validator Assignment

**Validator Agent**: {state['validator_agent'].value}
**Agent Guidelines**: docs/agents/REVIEW_AGENT.md

## Instructions

1. Read the agent guidelines at `docs/agents/REVIEW_AGENT.md`
2. Review the primary output at `.thursian/output/{task_id}_output.md`
3. Assess quality: correctness, completeness, clarity
4. Create validation file at: `.thursian/output/{task_id}_validation.md`
5. Mark status as either "**Status: APPROVED**" or "**Status: NEEDS_REVISION**"

## Expected Output

File: `.thursian/output/{task_id}_validation.md`

Format:
```markdown
# Validation: {task_id}

## Review Summary

[Overall assessment]

## Findings

- ✅ [What's good]
- ⚠️ [What needs attention]

## Recommendation

**Status: APPROVED**
(or **Status: NEEDS_REVISION**)

## Revision Notes

[If needs revision, specify what to change]
```

## Workflow Information

- Workflow ID: {state['workflow_id']}
- Task ID: {task_id}
- Primary Agent: {state['primary_agent'].value}
- Validator: {state['validator_agent'].value}
"""

        with open(validation_task_file, 'w') as f:
            f.write(validation_content)

        # Set expected validation file path
        validation_file_path = os.path.join(
            state['thursian_dir'],
            'output',
            f'{task_id}_validation.md'
        )

        logger.info(f"Created validation task: {validation_task_file}")
        print(f"\n{'='*60}")
        print(f"VALIDATION READY: {task_id}")
        print(f"Validation task: {validation_task_file}")
        print(f"Primary output: {state['output_file_path']}")
        print(f"Agent guidelines: docs/agents/REVIEW_AGENT.md")
        print(f"Validation file: {validation_file_path}")
        print(f"{'='*60}\n")

        result = {
            **add_decision_log(
                state,
                reasoning="Primary execution complete, assigned to review agent for validation",
                outcome=f"Waiting for validation at {validation_file_path}",
                agent_assigned=state['validator_agent'].value,
                doc_reference="docs/agents/REVIEW_AGENT.md",
                tool_used="file_creation"
            ),
            'validation_file_path': validation_file_path,
            'waiting_for_human': True
        }

        write_decision_log_to_file({**state, **result})
        update_status_file({**state, **result})

        return result

    except Exception as e:
        logger.error(f"Error in validation_node: {e}")
        return add_error(state, f"Validation node failed: {str(e)}")


def completion_node(state: ThursianState) -> Dict[str, Any]:
    """
    Finalize workflow.

    Logs completion decision and transitions to COMPLETED phase.
    Clears waiting_for_human flag.
    """
    logger.info(f"Completion node for task {state['current_task_id']}")

    try:
        logger.info(f"Workflow {state['workflow_id']} completed successfully")

        result = {
            **transition_phase(state, WorkflowPhase.COMPLETED),
            **add_decision_log(
                state,
                reasoning="Task validated and approved",
                outcome=f"Workflow completed successfully for task {state['current_task_id']}",
                tool_used="workflow_completion"
            ),
            'waiting_for_human': False,
            'validation_passed': True
        }

        write_decision_log_to_file({**state, **result})
        update_status_file({**state, **result})

        print(f"\n{'='*60}")
        print(f"WORKFLOW COMPLETE: {state['workflow_id']}")
        print(f"Task ID: {state['current_task_id']}")
        print(f"Status: ✅ Approved")
        print(f"{'='*60}\n")

        return result

    except Exception as e:
        logger.error(f"Error in completion_node: {e}")
        return add_error(state, f"Completion node failed: {str(e)}")
