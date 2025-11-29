# Thursian Orchestrator Test Suite

Comprehensive test suite for the Thursian development orchestrator.

## Test Structure

```
tests/
├── unit/                   # Unit tests for individual components
│   ├── test_state.py      # State definitions and enums
│   └── test_helpers.py    # Helper functions
├── integration/            # Integration tests for workflow components
│   ├── test_nodes.py      # Workflow node implementations
│   └── test_routing.py    # Conditional routing logic
├── e2e/                    # End-to-end workflow tests
│   └── test_workflow.py   # Complete workflow execution
└── run_tests.py           # Test runner script
```

## Running Tests

### All Tests

```bash
python -m tests.run_tests
```

### Specific Test Suites

```bash
# Unit tests only
python -m tests.run_tests --suite unit

# Integration tests only
python -m tests.run_tests --suite integration

# End-to-end tests only
python -m tests.run_tests --suite e2e
```

### Verbosity Levels

```bash
# Quiet (0)
python -m tests.run_tests --verbosity 0

# Normal (1)
python -m tests.run_tests --verbosity 1

# Verbose (2) - default
python -m tests.run_tests --verbosity 2
```

### Individual Test Files

```bash
# Run specific test file
python -m unittest tests.unit.test_state

# Run specific test class
python -m unittest tests.unit.test_state.TestWorkflowPhase

# Run specific test method
python -m unittest tests.unit.test_state.TestWorkflowPhase.test_phase_values
```

## Test Coverage

### Unit Tests (test_state.py, test_helpers.py)

**Coverage**:
- ✅ WorkflowPhase enum (all 6 phases)
- ✅ AgentRole enum (all 2 roles)
- ✅ DecisionLog TypedDict structure
- ✅ ThursianState TypedDict structure
- ✅ transition_phase() helper
- ✅ add_decision_log() helper
- ✅ add_error() helper
- ✅ write_decision_log_to_file() helper
- ✅ update_status_file() helper

**Total**: 15+ unit tests

### Integration Tests (test_nodes.py, test_routing.py)

**Coverage**:
- ✅ task_selection_node (success and error cases)
- ✅ assignment_node (agent assignment)
- ✅ execution_node (task file creation)
- ✅ validation_node (validation task creation)
- ✅ completion_node (workflow finalization)
- ✅ route_after_execution (all paths)
- ✅ route_after_validation (all paths)

**Total**: 15+ integration tests

### End-to-End Tests (test_workflow.py)

**Coverage**:
- ✅ Complete successful workflow cycle
- ✅ Workflow with revision cycle (NEEDS_REVISION → rework → APPROVED)

**Total**: 2 comprehensive E2E tests

## Expected Test Results

All tests should pass with no failures or errors:

```
======================================================================
THURSIAN ORCHESTRATOR TEST SUITE
======================================================================

Running: All Tests

...........................

----------------------------------------------------------------------
Ran 32 tests in X.XXXs

OK

======================================================================
TEST SUMMARY
======================================================================
Tests run: 32
Failures: 0
Errors: 0
Skipped: 0

✅ ALL TESTS PASSED!
```

## Test Scenarios

### Scenario 1: Happy Path

1. Task selection from queue
2. Agent assignment (coding + review)
3. Execution (task file created, human completes)
4. Validation (validation task created, human approves)
5. Completion (workflow finalized)

**Tested in**: `test_workflow.py::TestCompleteWorkflow::test_successful_workflow_cycle`

### Scenario 2: Revision Cycle

1. Task selection and assignment
2. First execution (incomplete implementation)
3. Validation rejects with NEEDS_REVISION
4. Return to execution
5. Second execution (fixed implementation)
6. Validation approves
7. Completion

**Tested in**: `test_workflow.py::TestCompleteWorkflow::test_workflow_with_revision`

### Scenario 3: Error Handling

- Empty task queue
- Missing output files
- Incomplete status markers
- File I/O errors

**Tested in**: Various unit and integration tests

## Adding New Tests

### Unit Test Template

```python
import unittest
from orchestrator.module import function_to_test

class TestMyFunction(unittest.TestCase):
    """Test my_function."""

    def test_basic_case(self):
        """Test basic functionality."""
        result = function_to_test(input)
        self.assertEqual(result, expected)

    def test_edge_case(self):
        """Test edge case handling."""
        with self.assertRaises(ValueError):
            function_to_test(invalid_input)
```

### Integration Test Template

```python
import unittest
import tempfile
import os
from orchestrator.nodes import my_node

class TestMyNode(unittest.TestCase):
    """Test my_node integration."""

    def test_node_execution(self):
        """Test node execution with files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Setup test state
            state = create_test_state(tmpdir)

            # Execute node
            result = my_node(state)

            # Verify results
            self.assertEqual(result['field'], expected)
            self.assertTrue(os.path.exists(expected_file))
```

## Continuous Integration

To integrate with CI/CD:

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: python -m tests.run_tests
```

## Test Dependencies

All tests use only Python standard library:
- `unittest` - Test framework
- `tempfile` - Temporary directories for file tests
- `os` - File system operations
- `json` - JSON validation

No additional dependencies required beyond `requirements.txt`.

## Troubleshooting

### Import Errors

**Error**: `ModuleNotFoundError: No module named 'orchestrator'`

**Solution**: Run from repository root:
```bash
python -m tests.run_tests
```

### File Permission Errors

**Error**: Permission denied when creating temp files

**Solution**: Ensure write permissions in test directory

### Tests Hang

**Error**: Tests hang during execution

**Solution**: Check for infinite loops in workflow logic (should not happen with proper routing)

## Performance

Expected test execution time:
- Unit tests: < 1 second
- Integration tests: < 5 seconds
- E2E tests: < 10 seconds
- **Total**: < 20 seconds

## Contributing

When adding new features:
1. Write unit tests for new functions
2. Write integration tests for new nodes
3. Update E2E tests if workflow changes
4. Ensure all tests pass before committing

---

**Test Suite Version**: 1.0
**Last Updated**: 2025-01-29
**Maintainer**: Automaton Development Team
