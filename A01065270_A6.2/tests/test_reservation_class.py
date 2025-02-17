import unittest
from unittest.mock import patch, mock_open
import json
from app.base_classes.reservation import Reservation


class TestReservation(unittest.TestCase):
    """Tests for the Reservation class."""

    @patch("builtins.open", new_callable=mock_open, read_data="[]")
    @patch("os.makedirs")
    def test_create_reservation(self, _mock_makedirs, _mock_file):
        """Test creating a reservation and ensuring it's saved."""
        with patch("app.base_classes.reservation.Reservation.load_from_file", return_value=[]):
            res = Reservation.create_reservation(1, 101, 201)
            self.assertIsInstance(res, Reservation)
            self.assertEqual(res.reservation_id, 1)
            self.assertEqual(res.customer_id, 101)
            self.assertEqual(res.hotel_id, 201)

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.exists", return_value=True)
    def test_load_reservations(self, _mock_exists, mock_file):
        """Test loading reservations from file."""
        reservation_data = json.dumps([{"reservation_id": 1, "customer_id": 101, "hotel_id": 201}])
        mock_file.return_value.read.return_value = reservation_data

        reservations = Reservation.load_from_file()
        self.assertEqual(len(reservations), 1)
        self.assertEqual(reservations[0].customer_id, 101)
        self.assertEqual(reservations[0].hotel_id, 201)

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps(
        [{"reservation_id": 1, "customer_id": 101, "hotel_id": 201}]
    ))
    @patch("os.path.exists", return_value=True)
    @patch("app.base_classes.reservation.Reservation.save_to_file")
    def test_cancel_reservation(self, mock_save, _mock_exists, _mock_file):
        """Test canceling a reservation."""
        with patch("app.base_classes.reservation.Reservation.load_from_file",
                   return_value=[Reservation(1, 101, 201)]):
            result = Reservation.cancel_reservation(1)

            # Assert that cancel_reservation() returns True
            self.assertTrue(result)

            # Ensure save_to_file() was called with an empty list (reservation was deleted)
            mock_save.assert_called_with([])

    @patch("app.config.debug_log")  # Correctly mock debug_log
    @patch("builtins.open", side_effect=IOError("Disk full"))  # Simulate disk error
    def test_save_to_file_error(self, mock_open, mock_debug_log):
        """Test handling of IOError when saving reservations."""
        reservations = [Reservation(1, 101, 201)]
        Reservation.save_to_file(reservations)


        # Correct assertion
        mock_debug_log.assert_called_with("Error saving reservations: Disk full")

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.exists", return_value=True)
    def test_save_to_file(self, _mock_exists, mock_file):
        """Test saving reservations to file."""
        reservations = [Reservation(1, 101, 201)]
        Reservation.save_to_file(reservations)
        mock_file.assert_called_once_with(Reservation.FILE_PATH, "w", encoding="utf-8")

    @patch("app.config.debug_log")
    def test_display_reservations_no_data(self, mock_debug_log):
        """Test displaying reservations when no reservations exist."""
        with patch("app.base_classes.reservation.Reservation.load_from_file", return_value=[]):
            Reservation.display_reservations()
            mock_debug_log.assert_called_with("No reservations found.")

    @patch("os.path.exists", return_value=False)
    def test_load_from_file_no_file(self, mock_exists):
        result = Reservation.load_from_file()
        self.assertEqual(result, [])

    @patch("builtins.open", side_effect=json.JSONDecodeError("Expecting value", "", 0))
    @patch("app.config.debug_log")
    def test_load_from_file_json_error(self, mock_debug_log, mock_open):
        result = Reservation.load_from_file()
        mock_debug_log.assert_called_with("Error loading reservations: Expecting value: line 1 column 1 (char 0)")
        self.assertEqual(result, [])

    @patch("app.base_classes.reservation.Reservation.load_from_file", return_value=[Reservation("123", "1", "1")])
    @patch("app.config.debug_log")
    def test_create_duplicate_reservation(self, mock_debug_log, mock_load):
        result = Reservation.create_reservation("123", "2", "2")
        mock_debug_log.assert_called_with("Reservation ID 123 already exists. Please choose a different ID.")
        self.assertFalse(result)

    @patch("app.base_classes.reservation.Reservation.load_from_file", return_value=[Reservation("123", "1", "1")])
    @patch("app.config.debug_log")
    def test_cancel_non_existent_reservation(self, mock_debug_log, mock_load):
        result = Reservation.cancel_reservation("999")
        mock_debug_log.assert_called_with("Reservation ID 999 not found.")
        self.assertFalse(result)

    @patch("app.base_classes.reservation.Reservation.load_from_file", return_value=[Reservation("123", "1", "1")])
    def test_find_by_id(self, mock_load):
        """Test finding a reservation by ID."""
        result = Reservation.find_by_id("123")
        self.assertIsNotNone(result)
        self.assertEqual(result.reservation_id, "123")

        # Test finding a non-existent reservation
        result = Reservation.find_by_id("999")
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()
