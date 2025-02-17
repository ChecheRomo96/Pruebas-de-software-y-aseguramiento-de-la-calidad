import unittest
from unittest.mock import patch, mock_open
import json
from app.base_classes.hotel import Hotel

class TestHotel(unittest.TestCase):
    """Tests for the Hotel class."""

    @patch("builtins.open", new_callable=mock_open, read_data="[]")
    @patch("os.makedirs")
    def test_create_hotel(self, _mock_makedirs, _mock_file):
        """Test creating a hotel and ensuring it's saved."""
        with patch("app.base_classes.hotel.Hotel.load_from_file", return_value=[]):
            hotel = Hotel.create_hotel(1, "Grand Hotel", "New York")
            self.assertIsInstance(hotel, Hotel)
            self.assertEqual(hotel.name, "Grand Hotel")
            self.assertEqual(hotel.location, "New York")

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.exists", return_value=True)
    def test_load_hotels(self, _mock_exists, mock_file):
        """Test loading hotels from file."""
        hotel_data = json.dumps([{"hotel_id": 1, "name": "Grand Hotel", "location": "New York"}])
        mock_file.return_value.read.return_value = hotel_data

        hotels = Hotel.load_from_file()
        self.assertEqual(len(hotels), 1)
        self.assertEqual(hotels[0].name, "Grand Hotel")

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.exists", return_value=True)
    def test_load_from_file_invalid_json(self, _mock_exists, mock_file):
        """Test handling of invalid JSON when loading hotels."""
        mock_file.return_value.read.return_value = "{invalid_json:}"
        
        with patch("builtins.print") as MockPrint:
            hotels = Hotel.load_from_file()
            MockPrint.assert_called()
            self.assertEqual(hotels, [])

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps(
        [{"hotel_id": 1, "name": "Grand Hotel", "location": "New York"}])
    )
    @patch("os.path.exists", return_value=True)
    @patch("app.base_classes.hotel.Hotel.save_to_file")
    def test_delete_hotel(self, mock_save, _mock_exists, _mock_file):
        """Test deleting a hotel."""
        with patch(
            "app.base_classes.hotel.Hotel.load_from_file",
            return_value=[Hotel(1, "Grand Hotel", "New York")]
        ):
            result = Hotel.delete_hotel(1)

            # Assert that delete_hotel() returns True
            self.assertTrue(result)

            # Ensure save_to_file() was called with an empty list (hotel was deleted)
            mock_save.assert_called_with([])

    @patch("app.base_classes.hotel.Hotel.load_from_file", return_value=[
        Hotel(1, "Grand Hotel", "New York")
    ])
    def test_find_by_id(self, _mock_load):
        """Test finding a hotel by ID."""
        hotel = Hotel.find_by_id(1)
        self.assertIsNotNone(hotel)
        self.assertEqual(hotel.name, "Grand Hotel")

        # Test non-existent hotel
        hotel = Hotel.find_by_id(999)
        self.assertIsNone(hotel)

    @patch("app.base_classes.hotel.Hotel.load_from_file", return_value=[
        Hotel(1, "Grand Hotel", "New York")
    ])
    @patch("app.base_classes.hotel.Hotel.save_to_file")
    def test_update_hotel(self, mock_save, _mock_load):
        """Test updating a hotel's name and location."""
        hotel = Hotel(1, "Grand Hotel", "New York")
        result = hotel.update(name="Updated Hotel", location="Los Angeles")

        self.assertTrue(result)
        mock_save.assert_called()

    @patch("app.base_classes.hotel.Hotel.load_from_file", return_value=[])
    @patch("app.base_classes.hotel.Hotel.save_to_file")
    def test_update_non_existent_hotel(self, mock_save, _mock_load):
        """Test updating a non-existent hotel."""
        hotel = Hotel(1, "Grand Hotel", "New York")
        result = hotel.update(name="Updated Hotel")
        self.assertFalse(result)
        mock_save.assert_not_called()

    @patch("builtins.open", side_effect=IOError("Disk full"))
    def test_save_to_file_error(self, MockOpen):
        """Test handling of IOError when saving hotels."""
        HotelList = [Hotel(1, "Grand Hotel", "New York")]

        with patch("builtins.print") as MockPrint:
            Hotel.save_to_file(HotelList)
            MockPrint.assert_called_with("Error saving hotels: Disk full")

    @patch("app.base_classes.hotel.Hotel.load_from_file", return_value=[
        Hotel(1, "Grand Hotel", "New York")
    ])
    @patch("app.base_classes.hotel.Hotel.save_to_file")
    def test_delete_instance_method(self, mock_save, _mock_load):
        """Test deleting a hotel using the instance method."""
        hotel = Hotel(1, "Grand Hotel", "New York")
        result = hotel.delete()
        self.assertTrue(result)
        mock_save.assert_called()

    @patch("app.config.debug_log")
    def test_display_hotels_no_data(self, mock_debug_log):
        """Test displaying hotels when no hotels exist."""
        with patch("app.base_classes.hotel.Hotel.load_from_file", return_value=[]):
            Hotel.display_hotels()
            mock_debug_log.assert_called_with("No hotels found.")

    @patch("app.base_classes.hotel.Hotel.load_from_file", return_value=[
        Hotel(1, "Grand Hotel", "New York"),
        Hotel(2, "City Inn", "Los Angeles")
    ])
    @patch("builtins.print")
    def test_display_hotels(self, mock_print, _mock_load):
        """Test displaying hotels."""
        Hotel.display_hotels()
        mock_print.assert_any_call("\n=== Available Hotels ===")
        mock_print.assert_any_call("ID: 0x0001 | Name: Grand Hotel | Location: New York")
        mock_print.assert_any_call("ID: 0x0002 | Name: City Inn | Location: Los Angeles")

    @patch("builtins.open", new_callable=mock_open, read_data="{invalid_json}")
    @patch("os.path.exists", return_value=True)
    def test_load_from_file_json_error(self, _mock_exists, mock_file):
        """Test that load_from_file handles JSONDecodeError."""
        with patch("builtins.print") as mock_print:
            hotels = Hotel.load_from_file()
            self.assertEqual(hotels, [])  # Should return an empty list
            mock_print.assert_called()  # Ensure the error message is printed
    
    @patch("app.base_classes.hotel.Hotel.load_from_file", return_value=[
        Hotel(1, "Grand Hotel", "New York")
    ])
    @patch("app.config.debug_log")
    def test_save_existing_hotel(self, mock_debug_log, _mock_load):
        """Test that save() prevents saving a duplicate hotel ID."""
        hotel = Hotel(1, "New Hotel", "Paris")  # ID 1 already exists
        result = hotel.save()
        self.assertFalse(result)
        mock_debug_log.assert_called_with("Hotel ID 1 already exists. Use `update()` instead.")

    @patch("app.base_classes.hotel.Hotel.load_from_file", return_value=[])
    @patch("app.base_classes.hotel.Hotel.save_to_file")
    @patch("app.config.debug_log")
    def test_save_new_hotel(self, mock_debug_log, mock_save, _mock_load):
        """Test saving a new hotel."""
        hotel = Hotel(1, "Grand Hotel", "New York")
        result = hotel.save()

        self.assertTrue(result)
        mock_save.assert_called()  # Ensure the file-saving method is called
        mock_debug_log.assert_called_with("Hotel Grand Hotel saved successfully.")

    @patch("app.base_classes.hotel.Hotel.load_from_file", return_value=[
        Hotel(1, "Grand Hotel", "New York")
    ])
    @patch("app.config.debug_log")
    def test_create_hotel_duplicate_id(self, mock_debug_log, _mock_load):
        """Test that create_hotel prevents duplicate hotel IDs."""
        result = Hotel.create_hotel(1, "Another Hotel", "Paris")  # ID 1 already exists
        self.assertFalse(result)
        mock_debug_log.assert_called_with("Hotel ID 1 already exists. Choose a different ID.")

    @patch("app.base_classes.hotel.Hotel.load_from_file", return_value=[
        Hotel(1, "Grand Hotel", "New York")
    ])
    @patch("app.config.debug_log")
    def test_delete_hotel_not_found(self, mock_debug_log, _mock_load):
        """Test that delete_hotel logs a message when trying to delete a non-existent hotel."""
        result = Hotel.delete_hotel(999)  # ID 999 does not exist
        self.assertFalse(result)
        mock_debug_log.assert_called_with("Hotel ID 999 not found.")

    @patch("os.path.exists", return_value=False)
    def test_load_from_file_no_file(self, mock_exists):
        """Test that load_from_file returns an empty list when the file does not exist."""
        hotels = Hotel.load_from_file()
        self.assertEqual(hotels, [])  # Should return an empty list

if __name__ == "__main__":
    unittest.main()
