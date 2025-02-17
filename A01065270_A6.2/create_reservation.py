"""
create_reservation.py

This script creates a new reservation with a unique ID in the hotel management system.

Usage:
    python create_reservation.py <Customer ID> <Hotel ID>

Author: José Manuel Romo
"""

import sys
import random
from app.base_classes.reservation import Reservation


def generate_unique_id():
    """
    Generate a random uint16 ID and ensure it is unique in the database.

    Returns:
        int: A unique 16-bit integer ID.
    """
    existing_reservations = Reservation.load_from_file()
    existing_ids = {res.reservation_id for res in existing_reservations}  # Set of existing IDs

    while True:
        new_id = random.randint(0, 65535)  # Generate a 16-bit integer ID
        if new_id not in existing_ids:  # Ensure uniqueness
            return new_id


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python create_reservation.py <Customer ID> <Hotel ID>")
        sys.exit(1)

    try:
        customer_id = int(sys.argv[1])  # Ensure Customer ID is an integer
        hotel_id = int(sys.argv[2])  # Ensure Hotel ID is an integer
    except ValueError:
        print("Error: Customer ID and Hotel ID must be integers.")
        sys.exit(1)

    reservation_id = generate_unique_id()  # Generate unique ID

    new_reservation = Reservation.create_reservation(reservation_id, customer_id, hotel_id)

    if new_reservation:
        print(f"Reservation created successfully with ID {reservation_id} "
              f"for Customer {customer_id} at Hotel {hotel_id}.")
    else:
        print("Failed to create reservation.")
