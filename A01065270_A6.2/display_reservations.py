"""
display_reservations.py

This script displays all reservations stored in the hotel management system.

Usage:
    python display_reservations.py

Author: José Manuel Romo
"""

from app.base_classes.reservation import Reservation

if __name__ == "__main__":
    try:
        Reservation.display_reservations()
    except AttributeError:
        print("Error: The Reservation class is not properly loaded.")
