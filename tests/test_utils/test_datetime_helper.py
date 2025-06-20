import unittest
import sys
import os

# Add the parent directory to the path so Python can find the src module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.utils.datetime_helper import calculate_duration_by_periods
from src.services.validation_service import ValidationService

class TestDatetimeHelper(unittest.TestCase):

    def setUp(self):
        """Set up the validation service instance for testing"""
        self.validation_service = ValidationService()

    def test_calculate_duration_by_periods(self):
        """Test duration calculation by periods"""
        # Setup test data
        arrival_time = self.validation_service.validate_datetime('2023-11-10 08:00')
        departure_time = self.validation_service.validate_datetime('2023-11-12 19:30')

        # Execute the function
        duration_breakdown = calculate_duration_by_periods(arrival_time, departure_time)
        
        # Assert the first period
        first_period = duration_breakdown[0]
        self.assertEqual(str(first_period[0]), '2023-11-10')  # date
        self.assertEqual(first_period[1], 'weekday')          # day_type
        self.assertEqual(first_period[2], '08:00-16:59')      # period
        self.assertEqual(first_period[3], 2)                  # hours
        self.assertEqual(first_period[4], 'normal')           # flag
        
        # Assert the second period
        second_period = duration_breakdown[1]
        self.assertEqual(str(second_period[0]), '2023-11-10')  # date
        self.assertEqual(second_period[1], 'weekday')          # day_type
        self.assertEqual(second_period[2], '08:00-16:59')      # period
        self.assertEqual(second_period[3], 7.0)                # hours
        self.assertEqual(second_period[4], 'exceed_time')      # flag

if __name__ == '__main__':
    unittest.main()