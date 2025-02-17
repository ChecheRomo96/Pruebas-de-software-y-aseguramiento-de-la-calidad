import json
import random
import os
import subprocess

def load_json(file_path):
    """Loads data from a JSON file if it exists."""
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error loading {file_path}: {e}")
        return []

def generate_reservations(num_reservations=10):
    """Generates reservation creation commands using real customer and hotel IDs."""
    customers = load_json("data/Customers.json")
    hotels = load_json("data/Hotels.json")
    
    if not customers or not hotels:
        print("No customers or hotels found. Ensure data/Customers.json and data/Hotels.json exist.")
        return
    
    commands = []
    for _ in range(num_reservations):
        customer = random.choice(customers)
        hotel = random.choice(hotels)
        
        customer_id = customer.get("customer_id")
        hotel_id = hotel.get("hotel_id")
        
        if customer_id is None or hotel_id is None:
            continue  # Skip invalid entries
        
        cmd = ["python3", "createReservation.py", str(customer_id), str(hotel_id)]
        commands.append(cmd)
    
    return commands

def execute_reservation_creation(commands):
    """Executes the generated reservation creation commands."""
    for cmd in commands:
        subprocess.run(cmd)

if __name__ == "__main__":
    num_reservations = 10  # Change this number to generate more or fewer reservations
    commands = generate_reservations(num_reservations)
    
    if commands:
        execute_reservation_creation(commands)
        print(f"{num_reservations} reservations created successfully.")
    else:
        print("No valid reservations could be created.")

