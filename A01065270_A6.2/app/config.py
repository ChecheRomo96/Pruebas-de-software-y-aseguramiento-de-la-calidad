"""
Configuration module for the application.

Contains global settings and utility functions.
"""

DEBUG = False  # Set to True to enable debug messages

def debug_log(message):
    """Conditionally prints debug messages if DEBUG is enabled globally."""
    if DEBUG:
        print(f"[DEBUG] {message}")
