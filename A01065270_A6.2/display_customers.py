"""
display_customers.py

This script displays all customers stored in the hotel management system.

Usage:
    python display_customers.py

Author: José Manuel Romo
"""

from app.base_classes.customer import Customer


if __name__ == "__main__":
    try:
        Customer.display_customers()
    except AttributeError:
        print("Error: The Customer class is not properly loaded.")
