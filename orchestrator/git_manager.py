"""Git commit automation for workflow traceability."""

import subprocess
from typing import Optional
import logging

logger = logging.getLogger(__name__)


def commit_phase(phase_name: str, task_id: Optional[str] = None) -> bool:
    """
    Create git commit for completed phase.

    Args:
        phase_name: Name of the workflow phase
        task_id: Optional task ID for context

    Returns:
        True if commit successful, False otherwise
    """
    try:
        message = f"Workflow: {phase_name}"
        if task_id:
            message += f" (task: {task_id})"

        # Add .thursian directory (contains decision logs and status)
        subprocess.run(
            ["git", "add", ".thursian/"],
            check=True,
            capture_output=True,
            text=True
        )

        # Create commit
        result = subprocess.run(
            ["git", "commit", "-m", message],
            check=True,
            capture_output=True,
            text=True
        )

        logger.info(f"Git commit created: {message}")
        return True

    except subprocess.CalledProcessError as e:
        # Check if it's just "nothing to commit"
        if "nothing to commit" in e.stderr or "nothing to commit" in e.stdout:
            logger.debug(f"No changes to commit for phase: {phase_name}")
            return True

        logger.error(f"Git commit failed: {e.stderr}")
        return False

    except Exception as e:
        logger.error(f"Git commit error: {e}")
        return False
