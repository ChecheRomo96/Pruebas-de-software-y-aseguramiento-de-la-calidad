import sys
import random
from app.base_classes.reservation import Reservation

def generate_unique_id():
    """Generate a random uint16 ID and ensure it is unique in the database."""
    existing_reservations = Reservation.load_from_file()
    existing_ids = {res.reservation_id for res in existing_reservations}  # Set of existing IDs

    while True:
        new_id = random.randint(0, 65535)  # Generate a 16-bit integer ID
        if new_id not in existing_ids:  # Ensure uniqueness
            return new_id

if __name__ == "__main__":
    # Ensure correct argument count
    if len(sys.argv) != 3:
        print("Usage: python createReservations.py <Customer ID> <Hotel ID>")
        sys.exit(1)

    customer_id = sys.argv[1]
    hotel_id = sys.argv[2]
    
    # Generate unique ID
    reservation_id = generate_unique_id()
    
    # Create the reservation
    new_reservation = Reservation.create_reservation(reservation_id, customer_id, hotel_id)
    
    if new_reservation:
        print(f"Reservation created successfully with ID {reservation_id} for Customer {customer_id} at Hotel {hotel_id}.")
    else:
        print("Failed to create reservation.")
