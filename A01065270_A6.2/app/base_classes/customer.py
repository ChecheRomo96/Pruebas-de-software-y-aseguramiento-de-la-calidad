import json
import os

class Customer:
    FILE_PATH = "customers.json"
    
    def __init__(self, customer_id, name, email):
        self.customer_id = customer_id
        self.name = name
        self.email = email
    
    def to_dict(self):
        return {"customer_id": self.customer_id, "name": self.name, "email": self.email}

    @classmethod
    def save_to_file(cls, customers):
        with open(cls.FILE_PATH, "w") as f:
            json.dump([customer.to_dict() for customer in customers], f)
    
    @classmethod
    def load_from_file(cls):
        if not os.path.exists(cls.FILE_PATH):
            return []
        with open(cls.FILE_PATH, "r") as f:
            return [cls(**customer) for customer in json.load(f)]
    
    @classmethod
    def create_customer(cls, customer_id, name, email):
        customers = cls.load_from_file()
        customers.append(cls(customer_id, name, email))
        cls.save_to_file(customers)
    
    @classmethod
    def delete_customer(cls, customer_id):
        customers = [customer for customer in cls.load_from_file() if customer.customer_id != customer_id]
        cls.save_to_file(customers)
    
    @classmethod
    def display_customers(cls):
        customers = cls.load_from_file()
        for customer in customers:
            print(f"ID: {customer.customer_id}, Name: {customer.name}, Email: {customer.email}")