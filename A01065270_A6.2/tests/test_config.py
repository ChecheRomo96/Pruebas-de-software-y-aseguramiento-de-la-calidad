import unittest
from unittest.mock import patch
import app.config as conf


class TestConfig(unittest.TestCase):

    @patch("builtins.print")
    def test_debug_log_enabled(self, mock_print):
        """Test that debug_log prints when DEBUG is True."""
        conf.DEBUG = True  # Enable debugging
        conf.debug_log("Test message")
        mock_print.assert_called_with("[DEBUG] Test message")

    @patch("builtins.print")
    def test_debug_log_disabled(self, mock_print):
        """Test that debug_log does not print when DEBUG is False."""
        conf.DEBUG = False  # Disable debugging
        conf.debug_log("Test message")
        mock_print.assert_not_called()  # Ensure no print was called

    def test_debug_log_function_exists(self):
        """Test that debug_log function is defined and callable."""
        self.assertTrue(callable(conf.debug_log))


if __name__ == "__main__":
    unittest.main()
