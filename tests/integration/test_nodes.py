"""Integration tests for workflow nodes."""

import unittest
import tempfile
import os
from datetime import datetime
from orchestrator.state import WorkflowPhase, AgentRole, ThursianState
from orchestrator.nodes import (
    task_selection_node,
    assignment_node,
    execution_node,
    validation_node,
    completion_node
)


class TestTaskSelectionNode(unittest.TestCase):
    """Test task_selection_node."""

    def test_task_selection_success(self):
        """Test successful task selection."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create task queue
            task_queue = os.path.join(tmpdir, 'task_queue.txt')
            with open(task_queue, 'w') as f:
                f.write("Test task 1\n")
                f.write("Test task 2\n")

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
                'thursian_dir': tmpdir,
                'output_file_path': None,
                'validation_file_path': None,
                'waiting_for_human': False,
                'validation_passed': False,
                'errors': []
            }

            result = task_selection_node(state)

            # Check phase transition
            self.assertEqual(result['current_phase'], WorkflowPhase.ASSIGNMENT)

            # Check task selected
            self.assertIsNotNone(result['current_task_id'])
            self.assertEqual(result['task_description'], 'Test task 1')

            # Check decision log
            self.assertEqual(len(result['decision_logs']), 1)

            # Check task queue updated
            with open(task_queue, 'r') as f:
                remaining = f.readlines()
                self.assertEqual(len(remaining), 1)
                self.assertEqual(remaining[0].strip(), 'Test task 2')

    def test_task_selection_empty_queue(self):
        """Test task selection with empty queue."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create empty task queue
            task_queue = os.path.join(tmpdir, 'task_queue.txt')
            with open(task_queue, 'w') as f:
                pass  # Empty file

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
                'thursian_dir': tmpdir,
                'output_file_path': None,
                'validation_file_path': None,
                'waiting_for_human': False,
                'validation_passed': False,
                'errors': []
            }

            result = task_selection_node(state)

            # Check error added
            self.assertIn('errors', result)
            self.assertTrue(len(result['errors']) > 0)


class TestAssignmentNode(unittest.TestCase):
    """Test assignment_node."""

    def test_agent_assignment(self):
        """Test agent assignment."""
        with tempfile.TemporaryDirectory() as tmpdir:
            state: ThursianState = {
                'workflow_id': 'test',
                'created_at': datetime.now(),
                'current_phase': WorkflowPhase.ASSIGNMENT,
                'phase_history': [],
                'current_task_id': 'task_123',
                'task_description': 'Test task',
                'task_file_path': None,
                'primary_agent': None,
                'validator_agent': None,
                'decision_logs': [],
                'thursian_dir': tmpdir,
                'output_file_path': None,
                'validation_file_path': None,
                'waiting_for_human': False,
                'validation_passed': False,
                'errors': []
            }

            result = assignment_node(state)

            # Check phase transition
            self.assertEqual(result['current_phase'], WorkflowPhase.EXECUTION)

            # Check agents assigned
            self.assertEqual(result['primary_agent'], AgentRole.CODING_AGENT)
            self.assertEqual(result['validator_agent'], AgentRole.REVIEW_AGENT)

            # Check decision log
            self.assertEqual(len(result['decision_logs']), 1)
            self.assertEqual(result['decision_logs'][0]['agent_assigned'], 'coding_agent')


class TestExecutionNode(unittest.TestCase):
    """Test execution_node."""

    def test_execution_creates_task_file(self):
        """Test execution node creates task file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            state: ThursianState = {
                'workflow_id': 'test_workflow',
                'created_at': datetime.now(),
                'current_phase': WorkflowPhase.EXECUTION,
                'phase_history': [],
                'current_task_id': 'task_123',
                'task_description': 'Write a test function',
                'task_file_path': None,
                'primary_agent': AgentRole.CODING_AGENT,
                'validator_agent': AgentRole.REVIEW_AGENT,
                'decision_logs': [],
                'thursian_dir': tmpdir,
                'output_file_path': None,
                'validation_file_path': None,
                'waiting_for_human': False,
                'validation_passed': False,
                'errors': []
            }

            result = execution_node(state)

            # Check task file created
            self.assertIn('task_file_path', result)
            task_file = result['task_file_path']
            self.assertTrue(os.path.exists(task_file))

            # Check task file content
            with open(task_file, 'r') as f:
                content = f.read()
                self.assertIn('task_123', content)
                self.assertIn('Write a test function', content)
                self.assertIn('CODING_AGENT.md', content)

            # Check waiting flag set
            self.assertTrue(result['waiting_for_human'])

            # Check output path set
            self.assertIn('output_file_path', result)


class TestValidationNode(unittest.TestCase):
    """Test validation_node."""

    def test_validation_creates_task_file(self):
        """Test validation node creates validation task."""
        with tempfile.TemporaryDirectory() as tmpdir:
            state: ThursianState = {
                'workflow_id': 'test_workflow',
                'created_at': datetime.now(),
                'current_phase': WorkflowPhase.VALIDATION,
                'phase_history': [],
                'current_task_id': 'task_456',
                'task_description': 'Test task',
                'task_file_path': None,
                'primary_agent': AgentRole.CODING_AGENT,
                'validator_agent': AgentRole.REVIEW_AGENT,
                'decision_logs': [],
                'thursian_dir': tmpdir,
                'output_file_path': os.path.join(tmpdir, 'output', 'task_456_output.md'),
                'validation_file_path': None,
                'waiting_for_human': False,
                'validation_passed': False,
                'errors': []
            }

            result = validation_node(state)

            # Check validation task file created
            validation_task = os.path.join(tmpdir, 'tasks', 'task_456_validation.md')
            self.assertTrue(os.path.exists(validation_task))

            # Check content
            with open(validation_task, 'r') as f:
                content = f.read()
                self.assertIn('task_456', content)
                self.assertIn('REVIEW_AGENT.md', content)

            # Check waiting flag
            self.assertTrue(result['waiting_for_human'])


class TestCompletionNode(unittest.TestCase):
    """Test completion_node."""

    def test_completion(self):
        """Test workflow completion."""
        with tempfile.TemporaryDirectory() as tmpdir:
            state: ThursianState = {
                'workflow_id': 'test_workflow',
                'created_at': datetime.now(),
                'current_phase': WorkflowPhase.VALIDATION,
                'phase_history': [],
                'current_task_id': 'task_789',
                'task_description': 'Test task',
                'task_file_path': None,
                'primary_agent': AgentRole.CODING_AGENT,
                'validator_agent': AgentRole.REVIEW_AGENT,
                'decision_logs': [],
                'thursian_dir': tmpdir,
                'output_file_path': None,
                'validation_file_path': None,
                'waiting_for_human': True,
                'validation_passed': False,
                'errors': []
            }

            result = completion_node(state)

            # Check phase transition
            self.assertEqual(result['current_phase'], WorkflowPhase.COMPLETED)

            # Check flags
            self.assertFalse(result['waiting_for_human'])
            self.assertTrue(result['validation_passed'])

            # Check decision log
            self.assertEqual(len(result['decision_logs']), 1)


if __name__ == '__main__':
    unittest.main()
