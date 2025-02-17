"""
hotel.py - A module for managing hotel information.

This module provides the `Hotel` class, which handles creating, storing,
retrieving, updating, and deleting hotel records in a JSON file.

Author: José Manuel Romo
"""

import json
import os

import app.config as conf


class Hotel:
    """Represents a hotel and provides methods to manage hotel records."""

    FILE_PATH = os.path.join("data", "Hotels.json")

    def __init__(self, hotel_id, name, location):
        """Initializes a new hotel instance."""
        self.hotel_id = hotel_id
        self.name = name
        self.location = location

    def to_dict(self):
        """Converts the hotel instance to a dictionary."""
        return {
            "hotel_id": self.hotel_id,
            "name": self.name,
            "location": self.location
        }

    @classmethod
    def ensure_data_directory(cls):
        """Ensures the 'data' directory exists before writing the file."""
        os.makedirs(os.path.dirname(cls.FILE_PATH), exist_ok=True)

    @classmethod
    def save_to_file(cls, hotels):
        """Saves a list of Hotel objects to a file in JSON format."""
        cls.ensure_data_directory()
        try:
            with open(cls.FILE_PATH, "w", encoding="utf-8") as f:
                json.dump([hotel.to_dict() for hotel in hotels], f, indent=4)
        except IOError as e:
            print(f"Error saving hotels: {e}")

    @classmethod
    def load_from_file(cls):
        """Loads hotels from a file and returns a list of Hotel objects."""
        if not os.path.exists(cls.FILE_PATH):
            return []
        try:
            with open(cls.FILE_PATH, "r", encoding="utf-8") as f:
                return [cls(**hotel) for hotel in json.load(f)]
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading hotels: {e}")
            return []

    @classmethod
    def create_hotel(cls, hotel_id, name, location):
        """Creates a new hotel and prevents duplicate IDs."""
        hotels = cls.load_from_file()
        if any(h.hotel_id == hotel_id for h in hotels):
            conf.debug_log(
                f"Hotel ID {hotel_id}"
                " already exists. Choose a different ID."
            )
            return False

        new_hotel = cls(hotel_id, name, location)
        hotels.append(new_hotel)
        cls.save_to_file(hotels)
        return new_hotel  # Return instance instead of True

    @classmethod
    def delete_hotel(cls, hotel_id):
        """Deletes a hotel by ID if it exists."""
        hotels = cls.load_from_file()
        new_hotels = [hotel for hotel in hotels if hotel.hotel_id != hotel_id]

        if len(new_hotels) == len(hotels):  # No hotel removed
            conf.debug_log(f"Hotel ID {hotel_id} not found.")
            return False

        cls.save_to_file(new_hotels)
        conf.debug_log(f"Hotel ID {hotel_id} deleted.")
        return True

    @classmethod
    def find_by_id(cls, hotel_id):
        """Finds a hotel by ID and returns an instance if found."""
        hotels = cls.load_from_file()
        for hotel in hotels:
            if hotel.hotel_id == hotel_id:
                return hotel
        return None

    def save(self):
        """Saves this hotel instance to the database."""
        hotels = Hotel.load_from_file()
        if any(h.hotel_id == self.hotel_id for h in hotels):
            conf.debug_log(
                f"Hotel ID {self.hotel_id} already exists."
                " Use `update()` instead."
            )
            return False

        hotels.append(self)
        Hotel.save_to_file(hotels)
        conf.debug_log(f"Hotel {self.name} saved successfully.")
        return True

    def update(self, name=None, location=None):
        """Updates this specific hotel's details in the database."""
        hotels = Hotel.load_from_file()
        for hotel in hotels:
            if hotel.hotel_id == self.hotel_id:
                if name:
                    hotel.name = name
                if location:
                    hotel.location = location
                Hotel.save_to_file(hotels)
                conf.debug_log(
                    f"Hotel {self.hotel_id} updated successfully."
                )
                return True
        conf.debug_log(f"Hotel ID {self.hotel_id} not found.")
        return False

    def delete(self):
        """Deletes this specific hotel from the database."""
        return Hotel.delete_hotel(self.hotel_id)

    @classmethod
    def display_hotels(cls):
        """Displays all hotels in a readable format."""
        hotels = cls.load_from_file()
        if not hotels:
            conf.debug_log("No hotels found.")
            return

        print("\n=== Available Hotels ===")
        for hotel in hotels:
            hex_id = f"0x{hotel.hotel_id:04X}"
            print(
                f"ID: {hex_id} "
                f"| Name: {hotel.name} "
                f"| Location: {hotel.location}"
            )
