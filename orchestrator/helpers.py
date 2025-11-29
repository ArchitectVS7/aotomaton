"""Helper functions for state transitions and logging."""

from typing import Dict, Any, Optional
from datetime import datetime
import os
import json

from .state import WorkflowPhase, DecisionLog, ThursianState


def transition_phase(state: ThursianState, new_phase: WorkflowPhase) -> Dict[str, Any]:
    """Helper to transition to a new phase and update phase history."""
    return {
        'current_phase': new_phase,
        'phase_history': [new_phase]  # Appends due to operator.add
    }


def add_decision_log(
    state: ThursianState,
    reasoning: str,
    outcome: str,
    agent_assigned: Optional[str] = None,
    doc_reference: Optional[str] = None,
    tool_used: Optional[str] = None
) -> Dict[str, Any]:
    """Add timestamped decision log to state."""
    log_entry: DecisionLog = {
        'task_id': state.get('current_task_id', 'unknown'),
        'timestamp': datetime.now().isoformat(),
        'phase': state['current_phase'].value,
        'agent_assigned': agent_assigned,
        'doc_reference': doc_reference,
        'tool_used': tool_used,
        'reasoning': reasoning,
        'outcome': outcome
    }

    return {'decision_logs': [log_entry]}


def add_error(state: ThursianState, error_message: str) -> Dict[str, Any]:
    """Add timestamped error to state."""
    return {
        'errors': [f"{datetime.now().isoformat()} - {error_message}"]
    }


def write_decision_log_to_file(state: ThursianState) -> None:
    """Write decision logs to .thursian/decisions/ directory."""
    if not state.get('decision_logs'):
        return

    decisions_dir = os.path.join(state['thursian_dir'], 'decisions')
    os.makedirs(decisions_dir, exist_ok=True)

    latest_log = state['decision_logs'][-1]
    timestamp = latest_log['timestamp'].replace(':', '-')
    filename = f"{timestamp}_{state['current_phase'].value}.json"
    filepath = os.path.join(decisions_dir, filename)

    with open(filepath, 'w') as f:
        json.dump(latest_log, f, indent=2)


def update_status_file(state: ThursianState) -> None:
    """Update .thursian/status.json with current state."""
    status = {
        'workflow_id': state['workflow_id'],
        'current_phase': state['current_phase'].value,
        'current_task_id': state.get('current_task_id'),
        'waiting_for_human': state.get('waiting_for_human', False),
        'last_updated': datetime.now().isoformat()
    }

    status_file = os.path.join(state['thursian_dir'], 'status.json')
    with open(status_file, 'w') as f:
        json.dump(status, f, indent=2)
