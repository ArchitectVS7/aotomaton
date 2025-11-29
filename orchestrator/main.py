"""CLI entry point for Thursian orchestrator."""

import time
from datetime import datetime
import logging
import sys

from .graph import create_thursian_workflow
from .state import ThursianState, WorkflowPhase
from .helpers import update_status_file
from .git_manager import commit_phase

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_workflow(thursian_dir: str = ".thursian", poll_interval: int = 5) -> None:
    """
    Run the Thursian orchestrator workflow.

    Args:
        thursian_dir: Path to .thursian directory (default: ".thursian")
        poll_interval: Seconds between polling checks (default: 5)
    """
    print("\n" + "="*60)
    print("THURSIAN DEVELOPMENT ORCHESTRATOR - MVP")
    print("="*60 + "\n")

    # Initialize state
    initial_state: ThursianState = {
        'workflow_id': f"workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        'created_at': datetime.now(),
        'current_phase': WorkflowPhase.IDLE,
        'phase_history': [],
        'current_task_id': None,
        'task_description': None,
        'task_file_path': None,
        'primary_agent': None,
        'validator_agent': None,
        'decision_logs': [],
        'thursian_dir': thursian_dir,
        'output_file_path': None,
        'validation_file_path': None,
        'waiting_for_human': False,
        'validation_passed': False,
        'errors': []
    }

    logger.info(f"Starting workflow: {initial_state['workflow_id']}")

    # Create workflow graph
    try:
        workflow = create_thursian_workflow()
    except Exception as e:
        logger.error(f"Failed to create workflow graph: {e}")
        print(f"\n❌ Error: Failed to create workflow graph: {e}")
        sys.exit(1)

    # Main execution loop with polling
    current_state = initial_state
    last_phase = None
    iteration_count = 0
    max_iterations = 1000  # Safety limit

    while current_state['current_phase'] != WorkflowPhase.COMPLETED and iteration_count < max_iterations:
        iteration_count += 1

        try:
            # Invoke workflow (single step)
            current_state = workflow.invoke(current_state)

            # Update status file
            update_status_file(current_state)

            # Check if phase changed
            if current_state['current_phase'] != last_phase:
                phase_name = current_state['current_phase'].value
                print(f"\n📍 Phase: {phase_name}")
                logger.info(f"Phase transition: {last_phase} → {phase_name}")

                # Git commit for phase transition
                commit_phase(phase_name, current_state.get('current_task_id'))

                last_phase = current_state['current_phase']

            # If waiting for human, poll
            if current_state.get('waiting_for_human'):
                phase = current_state['current_phase'].value
                print(f"⏳ Waiting for human to complete {phase}... (checking every {poll_interval}s)")
                time.sleep(poll_interval)

            # Check for errors
            if current_state.get('errors'):
                error_msg = current_state['errors'][-1]
                logger.error(f"Workflow error: {error_msg}")
                print(f"\n❌ Error: {error_msg}")
                break

        except KeyboardInterrupt:
            print("\n\n⚠️  Workflow interrupted by user")
            logger.info("Workflow interrupted by user")
            break

        except Exception as e:
            logger.error(f"Workflow execution error: {e}", exc_info=True)
            print(f"\n❌ Error: Workflow execution failed: {e}")
            break

    # Final status
    if current_state['current_phase'] == WorkflowPhase.COMPLETED:
        print("\n" + "="*60)
        print("✅ WORKFLOW COMPLETED SUCCESSFULLY")
        print(f"Workflow ID: {current_state['workflow_id']}")
        print(f"Task ID: {current_state['current_task_id']}")
        print(f"Iterations: {iteration_count}")
        print("="*60 + "\n")
        logger.info(f"Workflow completed: {current_state['workflow_id']}")
    elif iteration_count >= max_iterations:
        print(f"\n⚠️  Warning: Workflow exceeded max iterations ({max_iterations})")
        logger.warning(f"Workflow exceeded max iterations: {max_iterations}")
    else:
        print("\n⚠️  Workflow stopped before completion")
        logger.warning("Workflow stopped before completion")

    # Summary
    print("\nWorkflow Summary:")
    print(f"  - Decision logs: {len(current_state.get('decision_logs', []))}")
    print(f"  - Phase transitions: {len(current_state.get('phase_history', []))}")
    print(f"  - Errors: {len(current_state.get('errors', []))}")
    print()


if __name__ == "__main__":
    run_workflow()
