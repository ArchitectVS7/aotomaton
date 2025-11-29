"""Test runner for Thursian orchestrator test suite."""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def run_test_suite(verbosity=2):
    """
    Run the complete test suite.

    Args:
        verbosity: Test output verbosity (0=quiet, 1=normal, 2=verbose)

    Returns:
        TestResult object
    """
    # Discover and run all tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(__file__)
    suite = loader.discover(start_dir, pattern='test_*.py')

    # Run tests
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)

    return result


def run_unit_tests(verbosity=2):
    """Run only unit tests."""
    loader = unittest.TestLoader()
    start_dir = os.path.join(os.path.dirname(__file__), 'unit')
    suite = loader.discover(start_dir, pattern='test_*.py')
    runner = unittest.TextTestRunner(verbosity=verbosity)
    return runner.run(suite)


def run_integration_tests(verbosity=2):
    """Run only integration tests."""
    loader = unittest.TestLoader()
    start_dir = os.path.join(os.path.dirname(__file__), 'integration')
    suite = loader.discover(start_dir, pattern='test_*.py')
    runner = unittest.TextTestRunner(verbosity=verbosity)
    return runner.run(suite)


def run_e2e_tests(verbosity=2):
    """Run only end-to-end tests."""
    loader = unittest.TestLoader()
    start_dir = os.path.join(os.path.dirname(__file__), 'e2e')
    suite = loader.discover(start_dir, pattern='test_*.py')
    runner = unittest.TextTestRunner(verbosity=verbosity)
    return runner.run(suite)


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='Run Thursian orchestrator tests')
    parser.add_argument(
        '--suite',
        choices=['all', 'unit', 'integration', 'e2e'],
        default='all',
        help='Test suite to run (default: all)'
    )
    parser.add_argument(
        '--verbosity',
        type=int,
        choices=[0, 1, 2],
        default=2,
        help='Test output verbosity (default: 2)'
    )

    args = parser.parse_args()

    print("="*70)
    print("THURSIAN ORCHESTRATOR TEST SUITE")
    print("="*70)
    print()

    if args.suite == 'all':
        print("Running: All Tests")
        result = run_test_suite(args.verbosity)
    elif args.suite == 'unit':
        print("Running: Unit Tests Only")
        result = run_unit_tests(args.verbosity)
    elif args.suite == 'integration':
        print("Running: Integration Tests Only")
        result = run_integration_tests(args.verbosity)
    elif args.suite == 'e2e':
        print("Running: End-to-End Tests Only")
        result = run_e2e_tests(args.verbosity)

    print()
    print("="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    print()

    if result.wasSuccessful():
        print("[OK] ALL TESTS PASSED!")
        return 0
    else:
        print("[FAIL] SOME TESTS FAILED")
        return 1


if __name__ == '__main__':
    sys.exit(main())
