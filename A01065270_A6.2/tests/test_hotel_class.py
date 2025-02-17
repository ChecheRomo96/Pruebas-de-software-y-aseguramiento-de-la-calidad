"""
Unit tests for the Hotel class.
"""

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
            self.assertTrue(Hotel.create_hotel(1, "Grand Hotel", "New York"))


    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.exists", return_value=True)
    def test_load_hotels(self, _mock_exists, mock_file):
        """Test loading hotels from file."""
        hotel_data = json.dumps([{"hotel_id": 1, "name": "Grand Hotel", "location": "New York"}])
        mock_file.return_value.read.return_value = hotel_data

        hotels = Hotel.load_from_file()
        self.assertEqual(len(hotels), 1)
        self.assertEqual(hotels[0].name, "Grand Hotel")


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
    
    
    @patch("builtins.open", side_effect=IOError("Disk full"))
    def test_save_to_file_error(self, MockOpen):
        """Test handling of IOError when saving hotels."""
        HotelList = [Hotel(1, "Grand Hotel", "New York")]

        with patch("builtins.print") as MockPrint:
            Hotel.save_to_file(HotelList)
            MockPrint.assert_called_with("Error saving hotels: Disk full")


    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.exists", return_value=True)
    def test_save_to_file(self, _mock_exists, mock_file):
        """Test saving hotels to file."""
        hotel_list = [Hotel(1, "Grand Hotel", "New York")]
        Hotel.save_to_file(hotel_list)
        mock_file.assert_called_once_with(Hotel.FILE_PATH, "w", encoding="utf-8")


    @patch("app.config.debug_log")
    def test_display_hotels_no_data(self, mock_debug_log):
        """Test displaying hotels when no hotels exist."""
        with patch("app.base_classes.hotel.Hotel.load_from_file", return_value=[]):
            Hotel.display_hotels()
            mock_debug_log.assert_called_with("No hotels found.")


if __name__ == "__main__":
    unittest.main()
