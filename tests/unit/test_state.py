"""Unit tests for state definitions."""

import unittest
from datetime import datetime
from orchestrator.state import WorkflowPhase, AgentRole, ThursianState, DecisionLog


class TestWorkflowPhase(unittest.TestCase):
    """Test WorkflowPhase enum."""

    def test_phase_values(self):
        """Test all phase enum values exist."""
        self.assertEqual(WorkflowPhase.IDLE.value, "idle")
        self.assertEqual(WorkflowPhase.TASK_SELECTION.value, "task_selection")
        self.assertEqual(WorkflowPhase.ASSIGNMENT.value, "assignment")
        self.assertEqual(WorkflowPhase.EXECUTION.value, "execution")
        self.assertEqual(WorkflowPhase.VALIDATION.value, "validation")
        self.assertEqual(WorkflowPhase.COMPLETED.value, "completed")

    def test_phase_count(self):
        """Test expected number of phases."""
        phases = list(WorkflowPhase)
        self.assertEqual(len(phases), 6)


class TestAgentRole(unittest.TestCase):
    """Test AgentRole enum."""

    def test_agent_roles(self):
        """Test all agent role values exist."""
        self.assertEqual(AgentRole.CODING_AGENT.value, "coding_agent")
        self.assertEqual(AgentRole.REVIEW_AGENT.value, "review_agent")

    def test_agent_count(self):
        """Test expected number of agent roles."""
        roles = list(AgentRole)
        self.assertEqual(len(roles), 2)


class TestDecisionLog(unittest.TestCase):
    """Test DecisionLog TypedDict structure."""

    def test_decision_log_creation(self):
        """Test creating a decision log entry."""
        log: DecisionLog = {
            'task_id': 'test_task',
            'timestamp': datetime.now().isoformat(),
            'phase': 'execution',
            'agent_assigned': 'coding_agent',
            'doc_reference': 'docs/agents/CODING_AGENT.md',
            'tool_used': 'file_creation',
            'reasoning': 'Test reasoning',
            'outcome': 'Test outcome'
        }

        self.assertEqual(log['task_id'], 'test_task')
        self.assertEqual(log['phase'], 'execution')
        self.assertEqual(log['agent_assigned'], 'coding_agent')


class TestThursianState(unittest.TestCase):
    """Test ThursianState TypedDict structure."""

    def test_state_creation(self):
        """Test creating a minimal state."""
        state: ThursianState = {
            'workflow_id': 'test_workflow',
            'created_at': datetime.now(),
            'current_phase': WorkflowPhase.IDLE,
            'phase_history': [],
            'current_task_id': None,
            'task_description': None,
            'task_file_path': None,
            'primary_agent': None,
            'validator_agent': None,
            'decision_logs': [],
            'thursian_dir': '.thursian',
            'output_file_path': None,
            'validation_file_path': None,
            'waiting_for_human': False,
            'validation_passed': False,
            'errors': []
        }

        self.assertEqual(state['workflow_id'], 'test_workflow')
        self.assertEqual(state['current_phase'], WorkflowPhase.IDLE)
        self.assertEqual(state['waiting_for_human'], False)


if __name__ == '__main__':
    unittest.main()
