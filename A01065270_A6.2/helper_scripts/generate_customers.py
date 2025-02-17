"""
generate_customers.py

Script to generate random customers and add them to the system.
"""
import sys
import random
import subprocess

FIRST_NAMES = [
    "Alice", "Michael", "Sophie",
    "Daniel", "Emma", "James",
    "Olivia", "William", "Isabella", "Ethan"
]

LAST_NAMES = [
    "Johnson", "Smith", "Williams", "Brown",
    "Davis", "Wilson", "Martinez", "Anderson",
    "Thomas", "White"
]

EMAIL_DOMAINS = [
    "example.com", "mail.com", "test.com",
    "demo.org", "fakemail.net"
]

def generate_random_customer():
    """Generates a random customer name and email."""
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    email = f"{first_name.lower()}.{last_name.lower()}@{random.choice(EMAIL_DOMAINS)}"
    return f"{first_name} {last_name}", email

def generate_customers(num_customers=10):
    """Generates customer creation commands with random data."""
    commands = []
    for _ in range(num_customers):
        name, email = generate_random_customer()
        cmd = [sys.executable, "createCustomer.py", name, email]
        commands.append(cmd)
    return commands

def execute_customer_creation(commands):
    """Executes the generated customer creation commands in parallel."""
    processes = []

    for cmd in commands:
        # Ensure names with spaces are properly quoted
        cmd[1] = f'"{cmd[1]}"'
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        processes.append(process)

    # Wait for all processes to complete
    for process in processes:
        stdout, stderr = process.communicate()
        if stdout:
            print(stdout.strip())
        if stderr:
            print(stderr.strip())

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generateCustomers.py <num_customers>")
        sys.exit(1)

    try:
        n_customers = int(sys.argv[1])
        if n_customers <= 0:
            raise ValueError
    except ValueError:
        print("Error: <n_customers> must be a positive integer.")
        sys.exit(1)

    commands = generate_customers(n_customers)

    if commands:
        execute_customer_creation(commands)
        print(f"{n_customers} customers created successfully.")
    else:
        print("No valid customers could be created.")
