import json
import os

class Reservation:
    FILE_PATH = "reservations.json"
    
    def __init__(self, reservation_id, customer_id, hotel_id):
        self.reservation_id = reservation_id
        self.customer_id = customer_id
        self.hotel_id = hotel_id
    
    def to_dict(self):
        return {"reservation_id": self.reservation_id, "customer_id": self.customer_id, "hotel_id": self.hotel_id}

    @classmethod
    def save_to_file(cls, reservations):
        with open(cls.FILE_PATH, "w") as f:
            json.dump([reservation.to_dict() for reservation in reservations], f)
    
    @classmethod
    def load_from_file(cls):
        if not os.path.exists(cls.FILE_PATH):
            return []
        with open(cls.FILE_PATH, "r") as f:
            return [cls(**reservation) for reservation in json.load(f)]
    
    @classmethod
    def create_reservation(cls, reservation_id, customer_id, hotel_id):
        reservations = cls.load_from_file()
        reservations.append(cls(reservation_id, customer_id, hotel_id))
        cls.save_to_file(reservations)
    
    @classmethod
    def cancel_reservation(cls, reservation_id):
        reservations = [res for res in cls.load_from_file() if res.reservation_id != reservation_id]
        cls.save_to_file(reservations)
    
    @classmethod
    def display_reservations(cls):
        reservations = cls.load_from_file()
        for res in reservations:
            print(f"Reservation ID: {res.reservation_id}, Customer ID: {res.customer_id}, Hotel ID: {res.hotel_id}")
