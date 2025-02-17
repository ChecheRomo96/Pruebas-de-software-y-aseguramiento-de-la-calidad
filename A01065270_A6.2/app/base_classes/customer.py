"""
customer.py - A module for managing customer information.

This module provides the `Customer` class, which handles creating, storing,
retrieving, updating, and deleting customer records in a JSON file.

Author: José Manuel Romo
"""

import json
import os

import app.config as conf


class Customer:
    """Represents a customer and provides methods to manage customer records."""

    FILE_PATH = os.path.join("data", "Customers.json")

    def __init__(self, customer_id, name, email):
        """Initializes a new customer instance."""
        self.customer_id = customer_id
        self.name = name
        self.email = email

    def to_dict(self):
        """Converts the customer instance to a dictionary."""
        return {"customer_id": self.customer_id, "name": self.name, "email": self.email}

    @classmethod
    def ensure_data_directory(cls):
        """Ensures the 'data' directory exists before writing the file."""
        os.makedirs(os.path.dirname(cls.FILE_PATH), exist_ok=True)

    @classmethod
    def save_to_file(cls, customers):
        """Saves a list of Customer objects to a file in JSON format."""
        cls.ensure_data_directory()
        try:
            with open(cls.FILE_PATH, "w", encoding="utf-8") as f:
                json.dump([customer.to_dict() for customer in customers], f, indent=4)
        except IOError as e:
            conf.debug_log(f"Error saving customers: {e}")

    @classmethod
    def load_from_file(cls):
        """Loads customers from a file and returns a list of Customer objects."""
        if not os.path.exists(cls.FILE_PATH):
            return []
        try:
            with open(cls.FILE_PATH, "r", encoding="utf-8") as f:
                return [cls(**customer) for customer in json.load(f)]
        except (IOError, json.JSONDecodeError) as e:
            conf.debug_log(f"Error loading customers: {e}")
            return []

    @classmethod
    def create_customer(cls, customer_id, name, email):
        """Creates a new customer and prevents duplicate IDs."""
        customers = cls.load_from_file()
        if any(cust.customer_id == customer_id for cust in customers):
            conf.debug_log(f"Customer ID {customer_id} already exists. Choose a different ID.")
            return False

        new_customer = cls(customer_id, name, email)
        customers.append(new_customer)
        cls.save_to_file(customers)
        return new_customer

    @classmethod
    def delete_customer(cls, customer_id):
        """Deletes a customer by ID if it exists."""
        customers = cls.load_from_file()
        new_customers = [cust for cust in customers if cust.customer_id != customer_id]

        if len(new_customers) == len(customers):  # No customer removed
            conf.debug_log(f"Customer ID {customer_id} not found.")
            return False

        cls.save_to_file(new_customers)
        conf.debug_log(f"Customer ID {customer_id} deleted.")
        return True

    @classmethod
    def find_by_id(cls, customer_id):
        """Finds a customer by ID and returns an instance if found."""
        customers = cls.load_from_file()
        for cust in customers:
            if cust.customer_id == customer_id:
                return cust
        return None

    def save(self):
        """Saves this customer instance to the database."""
        customers = Customer.load_from_file()
        if any(cust.customer_id == self.customer_id for cust in customers):
            conf.debug_log(
                f"Customer ID {self.customer_id} already exists. Use `update()` instead."
            )
            return False

        customers.append(self)
        Customer.save_to_file(customers)
        conf.debug_log(f"Customer {self.name} saved successfully.")
        return True

    def delete(self):
        """Deletes this specific customer from the database."""
        return Customer.delete_customer(self.customer_id)

    @classmethod
    def display_customers(cls):
        """Displays all customers in a readable format."""
        customers = cls.load_from_file()
        if not customers:
            conf.debug_log("No customers found.")
            return

        print("\n=== Customer List ===")
        for cust in customers:
            print(f"ID: {cust.customer_id} | Name: {cust.name} | Email: {cust.email}")

    def update(self, name=None, email=None):
        """Updates this specific customer's details in the database."""
        customers = Customer.load_from_file()
        for cust in customers:
            if cust.customer_id == self.customer_id:
                if name:
                    cust.name = name
                if email:
                    cust.email = email
                Customer.save_to_file(customers)
                conf.debug_log(f"Customer {self.customer_id} updated successfully.")
                return True
        conf.debug_log(f"Customer ID {self.customer_id} not found.")
        return False
