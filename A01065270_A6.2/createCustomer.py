import sys
import random
from app.base_classes.customer import Customer

def generate_unique_id():
    """Generate a random uint16 ID and ensure it is unique in the database."""
    existing_customers = Customer.load_from_file()
    existing_ids = {cust.customer_id for cust in existing_customers}  # Set of existing IDs

    while True:
        new_id = random.randint(0, 65535)  # Generate a 16-bit integer ID
        if new_id not in existing_ids:  # Ensure uniqueness
            return new_id

if __name__ == "__main__":
    # Ensure correct argument count
    if len(sys.argv) != 3:
        print("Usage: python createCustomer.py <Customer Name> <Email>")
        sys.exit(1)

    customer_name = sys.argv[1]
    customer_email = sys.argv[2]
    
    # Generate unique ID
    customer_id = generate_unique_id()
    
    # Create the customer
    new_customer = Customer.create_customer(customer_id, customer_name, customer_email)
    
    if new_customer:
        print(f"Customer '{customer_name}' created successfully with ID {customer_id}.")
    else:
        print("Failed to create customer.")
