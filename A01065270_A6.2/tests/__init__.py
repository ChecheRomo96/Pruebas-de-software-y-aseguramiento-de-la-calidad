"""
tests/__init__.py - Test discovery setup for the unittest framework.

This module initializes test discovery and loads unit tests from the `tests` directory.
"""

import unittest

try:
    from .test_unit import TestHotel  # Ensure test_unit.py exists
except ImportError:
    TestHotel = None  # Avoid import errors if test_unit.py is missing

def load_tests(loader: unittest.TestLoader, _tests, _pattern) -> unittest.TestSuite:
    """
    Load and discover tests in the 'tests' directory.

    Args:
        loader (unittest.TestLoader): The test loader instance.
        tests (unittest.TestSuite): The current test suite.
        pattern (str): The test file matching pattern.

    Returns:
        unittest.TestSuite: The discovered test suite.
    """
    return loader.discover(start_dir="tests")  # Fix directory path
