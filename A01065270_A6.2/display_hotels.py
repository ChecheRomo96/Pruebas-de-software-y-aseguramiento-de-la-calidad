"""
display_hotels.py

This script displays all hotels stored in the hotel management system.

Usage:
    python display_hotels.py

Author: José Manuel Romo
"""

from app.base_classes.hotel import Hotel

if __name__ == "__main__":
    try:
        Hotel.display_hotels()
    except AttributeError:
        print("Error: The Hotel class is not properly loaded.")
