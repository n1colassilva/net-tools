"""Runs all tests in the tests directory"""
import sys
import unittest


def run_tests():
    """runs all tests"""
    # Discover and run all tests in the 'tests' directory
    test_suite = unittest.defaultTestLoader.discover("tests")
    runner = unittest.TextTestRunner()
    result = runner.run(test_suite)

    # Return exit code based on test results
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    EXIT_CODE = run_tests()
    sys.exit(EXIT_CODE)
