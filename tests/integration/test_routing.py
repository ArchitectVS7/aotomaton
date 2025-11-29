"""Integration tests for routing logic."""

import unittest
import tempfile
import os
from datetime import datetime
from orchestrator.state import WorkflowPhase, ThursianState
from orchestrator.routing import route_after_execution, route_after_validation


class TestRouteAfterExecution(unittest.TestCase):
    """Test route_after_execution routing function."""

    def test_loop_back_no_file(self):
        """Test loop back when output file doesn't exist."""
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
                'decision_logs': [],
                'thursian_dir': tmpdir,
                'output_file_path': os.path.join(tmpdir, 'output', 'task_123_output.md'),
                'validation_file_path': None,
                'waiting_for_human': False,
                'validation_passed': False,
                'errors': []
            }

            result = route_after_execution(state)
            self.assertEqual(result, "execution_node")  # Loop back

    def test_loop_back_incomplete(self):
        """Test loop back when output file exists but not marked complete."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = os.path.join(tmpdir, 'task_123_output.md')
            os.makedirs(os.path.dirname(output_file), exist_ok=True)

            with open(output_file, 'w') as f:
                f.write("# Output\n\nSome content but no status marker")

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
                'thursian_dir': tmpdir,
                'output_file_path': output_file,
                'validation_file_path': None,
                'waiting_for_human': False,
                'validation_passed': False,
                'errors': []
            }

            result = route_after_execution(state)
            self.assertEqual(result, "execution_node")  # Loop back

    def test_proceed_to_validation(self):
        """Test proceeding to validation when output is complete."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = os.path.join(tmpdir, 'task_123_output.md')
            os.makedirs(os.path.dirname(output_file), exist_ok=True)

            with open(output_file, 'w') as f:
                f.write("# Output\n\nImplementation here\n\n**Status: COMPLETE**")

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
                'thursian_dir': tmpdir,
                'output_file_path': output_file,
                'validation_file_path': None,
                'waiting_for_human': False,
                'validation_passed': False,
                'errors': []
            }

            result = route_after_execution(state)
            self.assertEqual(result, "validation_node")  # Proceed


class TestRouteAfterValidation(unittest.TestCase):
    """Test route_after_validation routing function."""

    def test_loop_back_no_file(self):
        """Test loop back when validation file doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            state: ThursianState = {
                'workflow_id': 'test',
                'created_at': datetime.now(),
                'current_phase': WorkflowPhase.VALIDATION,
                'phase_history': [],
                'current_task_id': 'task_456',
                'task_description': None,
                'task_file_path': None,
                'primary_agent': None,
                'validator_agent': None,
                'decision_logs': [],
                'thursian_dir': tmpdir,
                'output_file_path': None,
                'validation_file_path': os.path.join(tmpdir, 'validation', 'task_456_validation.md'),
                'waiting_for_human': False,
                'validation_passed': False,
                'errors': []
            }

            result = route_after_validation(state)
            self.assertEqual(result, "validation_node")  # Loop back

    def test_approved_proceeds_to_completion(self):
        """Test approved validation proceeds to completion."""
        with tempfile.TemporaryDirectory() as tmpdir:
            validation_file = os.path.join(tmpdir, 'task_456_validation.md')
            os.makedirs(os.path.dirname(validation_file), exist_ok=True)

            with open(validation_file, 'w') as f:
                f.write("# Validation\n\nLooks good!\n\n**Status: APPROVED**")

            state: ThursianState = {
                'workflow_id': 'test',
                'created_at': datetime.now(),
                'current_phase': WorkflowPhase.VALIDATION,
                'phase_history': [],
                'current_task_id': 'task_456',
                'task_description': None,
                'task_file_path': None,
                'primary_agent': None,
                'validator_agent': None,
                'decision_logs': [],
                'thursian_dir': tmpdir,
                'output_file_path': None,
                'validation_file_path': validation_file,
                'waiting_for_human': False,
                'validation_passed': False,
                'errors': []
            }

            result = route_after_validation(state)
            self.assertEqual(result, "completion")  # Proceed to completion

    def test_needs_revision_returns_to_execution(self):
        """Test needs revision returns to execution."""
        with tempfile.TemporaryDirectory() as tmpdir:
            validation_file = os.path.join(tmpdir, 'task_789_validation.md')
            os.makedirs(os.path.dirname(validation_file), exist_ok=True)

            with open(validation_file, 'w') as f:
                f.write("# Validation\n\nNeeds fixes\n\n**Status: NEEDS_REVISION**")

            state: ThursianState = {
                'workflow_id': 'test',
                'created_at': datetime.now(),
                'current_phase': WorkflowPhase.VALIDATION,
                'phase_history': [],
                'current_task_id': 'task_789',
                'task_description': None,
                'task_file_path': None,
                'primary_agent': None,
                'validator_agent': None,
                'decision_logs': [],
                'thursian_dir': tmpdir,
                'output_file_path': None,
                'validation_file_path': validation_file,
                'waiting_for_human': False,
                'validation_passed': False,
                'errors': []
            }

            result = route_after_validation(state)
            self.assertEqual(result, "execution_node")  # Return to execution


if __name__ == '__main__':
    unittest.main()
