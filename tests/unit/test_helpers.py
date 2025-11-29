"""Unit tests for helper functions."""

import unittest
import tempfile
import os
import json
from datetime import datetime
from orchestrator.state import WorkflowPhase, ThursianState
from orchestrator.helpers import (
    transition_phase,
    add_decision_log,
    add_error,
    write_decision_log_to_file,
    update_status_file
)


class TestTransitionPhase(unittest.TestCase):
    """Test transition_phase helper."""

    def test_phase_transition(self):
        """Test phase transition returns correct dict."""
        state: ThursianState = {
            'workflow_id': 'test',
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

        result = transition_phase(state, WorkflowPhase.TASK_SELECTION)

        self.assertIn('current_phase', result)
        self.assertIn('phase_history', result)
        self.assertEqual(result['current_phase'], WorkflowPhase.TASK_SELECTION)
        self.assertEqual(result['phase_history'], [WorkflowPhase.TASK_SELECTION])


class TestAddDecisionLog(unittest.TestCase):
    """Test add_decision_log helper."""

    def test_decision_log_creation(self):
        """Test decision log entry creation."""
        state: ThursianState = {
            'workflow_id': 'test',
            'created_at': datetime.now(),
            'current_phase': WorkflowPhase.EXECUTION,
            'phase_history': [],
            'current_task_id': 'task_123',
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

        result = add_decision_log(
            state,
            reasoning="Test reasoning",
            outcome="Test outcome",
            agent_assigned="coding_agent",
            doc_reference="docs/test.md",
            tool_used="test_tool"
        )

        self.assertIn('decision_logs', result)
        self.assertEqual(len(result['decision_logs']), 1)

        log = result['decision_logs'][0]
        self.assertEqual(log['task_id'], 'task_123')
        self.assertEqual(log['phase'], 'execution')
        self.assertEqual(log['agent_assigned'], 'coding_agent')
        self.assertEqual(log['reasoning'], 'Test reasoning')


class TestAddError(unittest.TestCase):
    """Test add_error helper."""

    def test_error_addition(self):
        """Test error message addition."""
        state: ThursianState = {
            'workflow_id': 'test',
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

        result = add_error(state, "Test error message")

        self.assertIn('errors', result)
        self.assertEqual(len(result['errors']), 1)
        self.assertIn('Test error message', result['errors'][0])


class TestWriteDecisionLogToFile(unittest.TestCase):
    """Test write_decision_log_to_file helper."""

    def test_write_decision_log(self):
        """Test writing decision log to file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            state: ThursianState = {
                'workflow_id': 'test',
                'created_at': datetime.now(),
                'current_phase': WorkflowPhase.EXECUTION,
                'phase_history': [],
                'current_task_id': 'task_123',
                'task_description': None,
                'task_file_path': None,
                'primary_agent': None,
                'validator_agent': None,
                'decision_logs': [{
                    'task_id': 'task_123',
                    'timestamp': '2025-01-29T10:00:00',
                    'phase': 'execution',
                    'agent_assigned': 'coding_agent',
                    'doc_reference': None,
                    'tool_used': 'test',
                    'reasoning': 'Test',
                    'outcome': 'Success'
                }],
                'thursian_dir': tmpdir,
                'output_file_path': None,
                'validation_file_path': None,
                'waiting_for_human': False,
                'validation_passed': False,
                'errors': []
            }

            write_decision_log_to_file(state)

            # Check file was created
            decisions_dir = os.path.join(tmpdir, 'decisions')
            self.assertTrue(os.path.exists(decisions_dir))

            files = os.listdir(decisions_dir)
            self.assertEqual(len(files), 1)

            # Check content
            with open(os.path.join(decisions_dir, files[0]), 'r') as f:
                log = json.load(f)
                self.assertEqual(log['task_id'], 'task_123')


class TestUpdateStatusFile(unittest.TestCase):
    """Test update_status_file helper."""

    def test_update_status(self):
        """Test updating status file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            state: ThursianState = {
                'workflow_id': 'workflow_123',
                'created_at': datetime.now(),
                'current_phase': WorkflowPhase.EXECUTION,
                'phase_history': [],
                'current_task_id': 'task_456',
                'task_description': None,
                'task_file_path': None,
                'primary_agent': None,
                'validator_agent': None,
                'decision_logs': [],
                'thursian_dir': tmpdir,
                'output_file_path': None,
                'validation_file_path': None,
                'waiting_for_human': True,
                'validation_passed': False,
                'errors': []
            }

            update_status_file(state)

            # Check file exists
            status_file = os.path.join(tmpdir, 'status.json')
            self.assertTrue(os.path.exists(status_file))

            # Check content
            with open(status_file, 'r') as f:
                status = json.load(f)
                self.assertEqual(status['workflow_id'], 'workflow_123')
                self.assertEqual(status['current_phase'], 'execution')
                self.assertEqual(status['current_task_id'], 'task_456')
                self.assertTrue(status['waiting_for_human'])


if __name__ == '__main__':
    unittest.main()
