import sys
import random
from app.base_classes.hotel import Hotel

def generate_unique_id():
    """Generate a random uint16 ID and ensure it is unique in the database."""
    existing_hotels = Hotel.load_from_file()
    existing_ids = {hotel.hotel_id for hotel in existing_hotels}  # Set of existing IDs

    while True:
        new_id = random.randint(0, 65535)  # Generate a 16bit integer ID
        if new_id not in existing_ids:  # Ensure uniqueness
            return new_id

if __name__ == "__main__":
    # Ensure correct argument count
    if len(sys.argv) != 3:
        print("Usage: python script.py <Hotel Name> <Location>")
        sys.exit(1)

    hotel_name = sys.argv[1]
    hotel_location = sys.argv[2]
    
    # Generate unique ID
    hotel_id = generate_unique_id()
    
    # Create the hotel
    new_hotel = Hotel.create_hotel(hotel_id, hotel_name, hotel_location)
    
    if new_hotel:
        print(f"Hotel '{hotel_name}' created successfully with ID {hotel_id}.")
    else:
        print("Failed to create hotel.")
