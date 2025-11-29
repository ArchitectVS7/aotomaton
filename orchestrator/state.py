"""State definitions for Thursian orchestrator workflow."""

from typing import TypedDict, Annotated, List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
import operator


class WorkflowPhase(str, Enum):
    """Workflow phase states."""
    IDLE = "idle"
    TASK_SELECTION = "task_selection"
    ASSIGNMENT = "assignment"
    EXECUTION = "execution"
    VALIDATION = "validation"
    COMPLETED = "completed"


class AgentRole(str, Enum):
    """Available agent roles."""
    CODING_AGENT = "coding_agent"
    REVIEW_AGENT = "review_agent"


class DecisionLog(TypedDict):
    """Structure for decision log entries."""
    task_id: str
    timestamp: str
    phase: str
    agent_assigned: Optional[str]
    doc_reference: Optional[str]
    tool_used: Optional[str]
    reasoning: str
    outcome: str


class ThursianState(TypedDict):
    """State for Thursian orchestrator workflow."""

    # Metadata
    workflow_id: str
    created_at: datetime

    # Current state
    current_phase: WorkflowPhase
    phase_history: Annotated[List[WorkflowPhase], operator.add]

    # Task context
    current_task_id: Optional[str]
    task_description: Optional[str]
    task_file_path: Optional[str]

    # Agent assignments
    primary_agent: Optional[AgentRole]
    validator_agent: Optional[AgentRole]

    # Decision logging (accumulates)
    decision_logs: Annotated[List[DecisionLog], operator.add]

    # File paths
    thursian_dir: str
    output_file_path: Optional[str]
    validation_file_path: Optional[str]

    # Flags
    waiting_for_human: bool
    validation_passed: bool

    # Error tracking (accumulates)
    errors: Annotated[List[str], operator.add]
