"""
cancel_reservation.py

Module for canceling reservations in the hotel management system.
"""

import app.config as conf
from app.base_classes.reservation import Reservation


def cancel_reservation(reservation_id):
    """Cancels a reservation by ID if it exists."""
    reservations = Reservation.load_from_file()
    new_reservations = [res for res in reservations if res.reservation_id != reservation_id]

    if len(new_reservations) == len(reservations):  # No reservation removed
        conf.debug_log(f"Reservation ID {reservation_id} not found.")
        return False

    Reservation.save_to_file(new_reservations)
    conf.debug_log(f"Reservation ID {reservation_id} canceled.")
    return True


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Cancel a reservation by ID.")
    parser.add_argument("reservation_id", type=str, help="The ID of the reservation to cancel.")
    args = parser.parse_args()

    if cancel_reservation(args.reservation_id):
        print(f"Reservation {args.reservation_id} successfully canceled.")
    else:
        print(f"Reservation {args.reservation_id} not found.")
