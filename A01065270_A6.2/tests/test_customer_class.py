import unittest
from unittest.mock import patch, mock_open
import json
from app.base_classes.customer import Customer

class TestCustomer(unittest.TestCase):
    """Tests for the Customer class."""

    @patch("builtins.open", new_callable=mock_open, read_data="[]")
    @patch("os.makedirs")
    def test_create_customer(self, _mock_makedirs, _mock_file):
        """Test creating a customer and ensuring it's saved."""
        with patch("app.base_classes.customer.Customer.load_from_file", return_value=[]):
            customer = Customer.create_customer(1, "Alice Johnson", "alice@example.com")
            self.assertIsInstance(customer, Customer)
            self.assertEqual(customer.name, "Alice Johnson")
            self.assertEqual(customer.email, "alice@example.com")

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.exists", return_value=True)
    def test_load_customers(self, _mock_exists, mock_file):
        """Test loading customers from file."""
        customer_data = json.dumps([{"customer_id": 1, "name": "Alice Johnson", "email": "alice@example.com"}])
        mock_file.return_value.read.return_value = customer_data

        customers = Customer.load_from_file()
        self.assertEqual(len(customers), 1)
        self.assertEqual(customers[0].name, "Alice Johnson")

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.exists", return_value=True)
    def test_load_from_file_invalid_json(self, _mock_exists, mock_file):
        """Test handling of invalid JSON when loading customers."""
        mock_file.return_value.read.return_value = "{invalid_json:}"

        with patch("app.config.debug_log") as mock_debug_log:
            customers = Customer.load_from_file()
            self.assertEqual(customers, [])
            mock_debug_log.assert_called()

    @patch("app.base_classes.customer.Customer.load_from_file", return_value=[
        Customer(1, "Alice Johnson", "alice@example.com")
    ])
    @patch("app.base_classes.customer.Customer.save_to_file")
    def test_delete_customer(self, mock_save, _mock_load):
        """Test deleting a customer."""
        result = Customer.delete_customer(1)
        self.assertTrue(result)
        mock_save.assert_called_with([])

    @patch("app.base_classes.customer.Customer.load_from_file", return_value=[
        Customer(1, "Alice Johnson", "alice@example.com")
    ])
    @patch("app.config.debug_log")
    def test_delete_customer_not_found(self, mock_debug_log, _mock_load):
        """Test deleting a non-existent customer."""
        result = Customer.delete_customer(999)
        self.assertFalse(result)
        mock_debug_log.assert_called_with("Customer ID 999 not found.")

    @patch("app.base_classes.customer.Customer.load_from_file", return_value=[
        Customer(1, "Alice Johnson", "alice@example.com")
    ])
    def test_find_by_id(self, _mock_load):
        """Test finding a customer by ID."""
        customer = Customer.find_by_id(1)
        self.assertIsNotNone(customer)
        self.assertEqual(customer.name, "Alice Johnson")

        customer = Customer.find_by_id(999)
        self.assertIsNone(customer)

    @patch("app.base_classes.customer.Customer.load_from_file", return_value=[
        Customer(1, "Alice Johnson", "alice@example.com")
    ])
    @patch("app.base_classes.customer.Customer.save_to_file")
    def test_update_customer(self, mock_save, _mock_load):
        """Test updating a customer's details."""
        customer = Customer(1, "Alice Johnson", "alice@example.com")
        result = customer.update(name="Updated Alice", email="alice@newdomain.com")

        self.assertTrue(result)
        mock_save.assert_called()

    @patch("app.base_classes.customer.Customer.load_from_file", return_value=[])
    @patch("app.base_classes.customer.Customer.save_to_file")
    def test_update_non_existent_customer(self, mock_save, _mock_load):
        """Test updating a non-existent customer."""
        customer = Customer(1, "Alice Johnson", "alice@example.com")
        result = customer.update(name="Updated Alice")
        self.assertFalse(result)
        mock_save.assert_not_called()

    @patch("builtins.open", side_effect=IOError("Disk full"))
    def test_save_to_file_error(self, MockOpen):
        """Test handling of IOError when saving customers."""
        CustomerList = [Customer(1, "Alice Johnson", "alice@example.com")]

        with patch("app.config.debug_log") as mock_debug_log:
            Customer.save_to_file(CustomerList)
            mock_debug_log.assert_called_with("Error saving customers: Disk full")

    @patch("app.base_classes.customer.Customer.load_from_file", return_value=[
        Customer(1, "Alice Johnson", "alice@example.com")
    ])
    @patch("app.base_classes.customer.Customer.save_to_file")
    def test_delete_instance_method(self, mock_save, _mock_load):
        """Test deleting a customer using the instance method."""
        customer = Customer(1, "Alice Johnson", "alice@example.com")
        result = customer.delete()
        self.assertTrue(result)
        mock_save.assert_called()

    @patch("app.config.debug_log")
    def test_display_customers_no_data(self, mock_debug_log):
        """Test displaying customers when no customers exist."""
        with patch("app.base_classes.customer.Customer.load_from_file", return_value=[]):
            Customer.display_customers()
            mock_debug_log.assert_called_with("No customers found.")

    @patch("app.base_classes.customer.Customer.load_from_file", return_value=[
        Customer(1, "Alice Johnson", "alice@example.com"),
        Customer(2, "Bob Smith", "bob@example.com")
    ])
    @patch("builtins.print")
    def test_display_customers(self, mock_print, _mock_load):
        """Test displaying customers."""
        Customer.display_customers()
        mock_print.assert_any_call("\n=== Customer List ===")
        mock_print.assert_any_call("ID: 1 | Name: Alice Johnson | Email: alice@example.com")
        mock_print.assert_any_call("ID: 2 | Name: Bob Smith | Email: bob@example.com")


if __name__ == "__main__":
    unittest.main()
