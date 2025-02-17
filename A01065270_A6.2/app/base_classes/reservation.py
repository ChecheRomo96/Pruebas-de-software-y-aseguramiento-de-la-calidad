"""
reservation.py - A module for managing hotel reservations.

This module provides the `Reservation` class, which handles creating, storing,
retrieving, updating, and deleting hotel reservations in a JSON file.

Author: José Manuel Romo
"""

import json
import os

import app.config as conf
from app.base_classes.hotel import Hotel
from app.base_classes.customer import Customer

class Reservation:
    """Represents a reservation and provides methods to manage reservations."""

    FILE_PATH = os.path.join("data", "Reservations.json")

    def __init__(self, reservation_id, customer_id, hotel_id):
        """Initializes a new reservation instance."""
        self.reservation_id = reservation_id
        self.customer_id = customer_id
        self.hotel_id = hotel_id

    def to_dict(self):
        """Converts the reservation instance to a dictionary."""
        return {
            "reservation_id": self.reservation_id,
            "customer_id": self.customer_id,
            "hotel_id": self.hotel_id,
        }

    @classmethod
    def ensure_data_directory(cls):
        """Ensures the 'data' directory exists before writing the file."""
        os.makedirs(os.path.dirname(cls.FILE_PATH), exist_ok=True)

    @classmethod
    def save_to_file(cls, reservations):
        """Saves a list of Reservation objects to a file in JSON format."""
        cls.ensure_data_directory()
        try:
            with open(cls.FILE_PATH, "w", encoding="utf-8") as f:
                json.dump([res.to_dict() for res in reservations], f, indent=4)
        except IOError as e:
            conf.debug_log(f"Error saving reservations: {e}")

    @classmethod
    def load_from_file(cls):
        """Loads reservations from a file and returns a list of Reservation objects."""
        if not os.path.exists(cls.FILE_PATH):
            return []
        try:
            with open(cls.FILE_PATH, "r", encoding="utf-8") as f:
                return [cls(**res) for res in json.load(f)]
        except (IOError, json.JSONDecodeError) as e:
            conf.debug_log(f"Error loading reservations: {e}")
            return []

    @classmethod
    def create_reservation(cls, reservation_id, customer_id, hotel_id):
        """Creates a new reservation and prevents duplicate IDs."""
        reservations = cls.load_from_file()
        if any(res.reservation_id == reservation_id for res in reservations):
            conf.debug_log(
                f"Reservation ID {reservation_id} already exists. "
                "Please choose a different ID."
            )
            return False

        new_reservation = cls(reservation_id, customer_id, hotel_id)
        reservations.append(new_reservation)
        cls.save_to_file(reservations)
        return new_reservation

    @classmethod
    def cancel_reservation(cls, reservation_id):
        """Cancels a reservation by ID if it exists."""
        reservations = cls.load_from_file()
        new_reservations = [res for res in reservations if res.reservation_id != reservation_id]

        if len(new_reservations) == len(reservations):  # No reservation removed
            conf.debug_log(f"Reservation ID {reservation_id} not found.")
            return False

        cls.save_to_file(new_reservations)
        conf.debug_log(f"Reservation ID {reservation_id} canceled.")
        return True

    @classmethod
    def find_by_id(cls, reservation_id):
        """Finds a reservation by ID and returns an instance if found."""
        reservations = cls.load_from_file()
        for res in reservations:
            if res.reservation_id == reservation_id:
                return res
        return None

    def save(self):
        """Saves this reservation instance to the database."""
        reservations = Reservation.load_from_file()
        if any(res.reservation_id == self.reservation_id for res in reservations):
            conf.debug_log(
                f"Reservation ID {self.reservation_id} already exists. "
                f"Use `update()` instead."
            )
            return False

        reservations.append(self)
        Reservation.save_to_file(reservations)
        conf.debug_log(f"Reservation {self.reservation_id} saved successfully.")
        return True

    def delete(self):
        """Deletes this specific reservation from the database."""
        return Reservation.cancel_reservation(self.reservation_id)

    @classmethod
    def display_reservations(cls):
        """Displays all reservations in a readable format."""
        reservations = cls.load_from_file()
        customers = {c.customer_id: c.name for c in Customer.load_from_file()}
        hotels = {h.hotel_id: h.name for h in Hotel.load_from_file()}

        if not reservations:
            conf.debug_log("No reservations found.")
            return

        print("\n=== Current Reservations ===")
        for res in reservations:
            customer_name = customers.get(res.customer_id, "Unknown Customer")
            hotel_name = hotels.get(res.hotel_id, "Unknown Hotel")
            print(
                f"Reservation ID: {res.reservation_id} | "
                f"Customer: {customer_name} | Hotel: {hotel_name}"
            )
