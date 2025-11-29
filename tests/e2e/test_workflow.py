"""End-to-end workflow test."""

import unittest
import tempfile
import os
from datetime import datetime
from orchestrator.state import WorkflowPhase, AgentRole, ThursianState
from orchestrator.graph import create_thursian_workflow


class TestCompleteWorkflow(unittest.TestCase):
    """Test complete workflow execution."""

    def test_successful_workflow_cycle(self):
        """Test a complete successful workflow cycle."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Setup task queue
            task_queue = os.path.join(tmpdir, 'task_queue.txt')
            with open(task_queue, 'w') as f:
                f.write("Write a Python function to reverse a string\n")

            # Initialize state
            initial_state: ThursianState = {
                'workflow_id': f"test_workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
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

            # Create workflow
            workflow = create_thursian_workflow()

            # Execute: Task Selection
            state = workflow.invoke(initial_state)
            self.assertEqual(state['current_phase'], WorkflowPhase.ASSIGNMENT)
            self.assertIsNotNone(state['current_task_id'])
            task_id = state['current_task_id']

            # Execute: Assignment
            state = workflow.invoke(state)
            self.assertEqual(state['current_phase'], WorkflowPhase.EXECUTION)
            self.assertEqual(state['primary_agent'], AgentRole.CODING_AGENT)
            self.assertEqual(state['validator_agent'], AgentRole.REVIEW_AGENT)

            # Execute: Execution (creates task file, waits for human)
            state = workflow.invoke(state)
            self.assertTrue(state['waiting_for_human'])
            task_file = state['task_file_path']
            self.assertTrue(os.path.exists(task_file))

            # Simulate human completing task
            output_file = state['output_file_path']
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, 'w') as f:
                f.write("""# Task Output: {task_id}

## Implementation

```python
def reverse_string(s: str) -> str:
    \"\"\"Reverse a string.\"\"\"
    return s[::-1]
```

## Notes

Used Python slicing for simplicity.

**Status: COMPLETE**
""".format(task_id=task_id))

            # Execute: Execution (detects completion, proceeds to validation)
            state = workflow.invoke(state)
            self.assertEqual(state['current_phase'], WorkflowPhase.VALIDATION)

            # Execute: Validation (creates validation task, waits for human)
            state = workflow.invoke(state)
            self.assertTrue(state['waiting_for_human'])
            validation_task = os.path.join(tmpdir, 'tasks', f'{task_id}_validation.md')
            self.assertTrue(os.path.exists(validation_task))

            # Simulate human validation
            validation_file = state['validation_file_path']
            os.makedirs(os.path.dirname(validation_file), exist_ok=True)
            with open(validation_file, 'w') as f:
                f.write("""# Validation: {task_id}

## Review Summary

Implementation is correct and follows best practices.

## Findings

### ✅ Strengths
- Correct implementation
- Clean code
- Good documentation

### ⚠️ Issues
None

## Recommendation

**Status: APPROVED**
""".format(task_id=task_id))

            # Execute: Validation (detects approval, proceeds to completion)
            state = workflow.invoke(state)
            self.assertEqual(state['current_phase'], WorkflowPhase.COMPLETED)

            # Execute: Completion
            state = workflow.invoke(state)
            self.assertEqual(state['current_phase'], WorkflowPhase.COMPLETED)
            self.assertFalse(state['waiting_for_human'])
            self.assertTrue(state['validation_passed'])

            # Verify decision logs
            self.assertGreater(len(state['decision_logs']), 0)

            # Verify phase history
            self.assertIn(WorkflowPhase.TASK_SELECTION, state['phase_history'])
            self.assertIn(WorkflowPhase.ASSIGNMENT, state['phase_history'])
            self.assertIn(WorkflowPhase.EXECUTION, state['phase_history'])
            self.assertIn(WorkflowPhase.VALIDATION, state['phase_history'])
            self.assertIn(WorkflowPhase.COMPLETED, state['phase_history'])

    def test_workflow_with_revision(self):
        """Test workflow with revision cycle."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Setup task queue
            task_queue = os.path.join(tmpdir, 'task_queue.txt')
            with open(task_queue, 'w') as f:
                f.write("Implement factorial function\n")

            # Initialize state
            initial_state: ThursianState = {
                'workflow_id': f"test_revision_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
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

            # Create workflow
            workflow = create_thursian_workflow()

            # Execute workflow to execution phase
            state = workflow.invoke(initial_state)  # Task selection
            state = workflow.invoke(state)  # Assignment
            state = workflow.invoke(state)  # Execution (create task)
            task_id = state['current_task_id']

            # First attempt - incomplete implementation
            output_file = state['output_file_path']
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, 'w') as f:
                f.write("""# Task Output: {task_id}

## Implementation

```python
def factorial(n):
    return n * factorial(n - 1)
```

**Status: COMPLETE**
""".format(task_id=task_id))

            # Proceed to validation
            state = workflow.invoke(state)
            state = workflow.invoke(state)

            # Validation - needs revision
            validation_file = state['validation_file_path']
            os.makedirs(os.path.dirname(validation_file), exist_ok=True)
            with open(validation_file, 'w') as f:
                f.write("""# Validation: {task_id}

## Review Summary

Missing base case - will cause infinite recursion.

## Findings

### ⚠️ Issues
- No base case for n=0 or n=1
- Will crash on execution

**Status: NEEDS_REVISION**

## Revision Notes

Add base case: if n <= 1: return 1
""".format(task_id=task_id))

            # Should return to execution
            state = workflow.invoke(state)
            self.assertEqual(state['current_phase'], WorkflowPhase.EXECUTION)

            # Second attempt - fixed implementation
            with open(output_file, 'w') as f:
                f.write("""# Task Output: {task_id}

## Implementation

```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

## Notes

Added base case as requested.

**Status: COMPLETE**
""".format(task_id=task_id))

            # Proceed to validation again
            state = workflow.invoke(state)
            state = workflow.invoke(state)

            # Validation - approved
            with open(validation_file, 'w') as f:
                f.write("""# Validation: {task_id}

## Review Summary

Now correct with proper base case.

**Status: APPROVED**
""".format(task_id=task_id))

            # Should complete
            state = workflow.invoke(state)
            self.assertEqual(state['current_phase'], WorkflowPhase.COMPLETED)


if __name__ == '__main__':
    unittest.main()
