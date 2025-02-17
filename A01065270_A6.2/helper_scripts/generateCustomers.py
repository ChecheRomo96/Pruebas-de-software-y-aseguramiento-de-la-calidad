
import sys
import json
import random
import os
import subprocess

FIRST_NAMES = ["Alice", "Michael", "Sophie", "Daniel", "Emma", "James", "Olivia", "William", "Isabella", "Ethan"]
LAST_NAMES = ["Johnson", "Smith", "Williams", "Brown", "Davis", "Wilson", "Martinez", "Anderson", "Thomas", "White"]
EMAIL_DOMAINS = ["example.com", "mail.com", "test.com", "demo.org", "fakemail.net"]

def generate_random_customer():
    """Generates a random customer name and email."""
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    email = f"{first_name.lower()}.{last_name.lower()}@{random.choice(EMAIL_DOMAINS)}"
    return first_name + " " + last_name, email

def generate_customers(num_customers=10):
    """Generates customer creation commands with random data."""
    commands = []
    for _ in range(num_customers):
        name, email = generate_random_customer()
        cmd = ["python3", "createCustomer.py", name, email]
        commands.append(cmd)
    return commands

def execute_customer_creation(commands):
    """Executes the generated customer creation commands."""
    for cmd in commands:
        subprocess.run(cmd)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generateCustomers.py <num_customers>")
        sys.exit(1)
    
    try:
        num_customers = int(sys.argv[1])
        if num_customers <= 0:
            raise ValueError
    except ValueError:
        print("Error: <num_customers> must be a positive integer.")
        sys.exit(1)
    
    commands = generate_customers(num_customers)
    
    if commands:
        execute_customer_creation(commands)
        print(f"{num_customers} customers created successfully.")
    else:
        print("No valid customers could be created.")
