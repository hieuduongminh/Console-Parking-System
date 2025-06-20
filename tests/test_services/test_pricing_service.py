import unittest
import sys
import os

# Add the parent directory to the path so Python can find the src module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.services.pricing_service import PricingService
from src.services.validation_service import ValidationService

class TestPricingService(unittest.TestCase):
   
    def setUp(self):
        """Set up the PricingService instance for testing"""
        self.pricing_service = PricingService()
        self.validation_service = ValidationService()

    def test_get_parking_fee(self):
        """Test calculating parking fee for different durations"""
        
        arrival_time  = self.validation_service.validate_datetime('2023-11-10 08:00')
        departure_time = self.validation_service.validate_datetime('2023-11-12 19:30')
        has_frequent_parking = False

        # Calculate parking fee 
        fee, calculation_details = self.pricing_service.calculate_parking_fee(arrival_time=arrival_time,
                                                         departure_time=departure_time,
                                                         has_frequent_parking=has_frequent_parking)
        # Check if the fee is calculated correctly
        self.assertEqual(fee, 347.00)

    def test_get_parking_fee_with_has_frequent_parking(self):
        """Test calculating parking fee with frequent parking"""
        
        arrival_time  = self.validation_service.validate_datetime('2023-11-10 08:00')
        departure_time = self.validation_service.validate_datetime('2023-11-12 19:30')
        has_frequent_parking = True

        # Calculate parking fee 
        fee, calculation_details = self.pricing_service.calculate_parking_fee(arrival_time=arrival_time,
                                                         departure_time=departure_time,
                                                         has_frequent_parking=has_frequent_parking)
        # Check if the fee is calculated correctly
        self.assertEqual(fee, 262.30)


if __name__ == '__main__':
    unittest.main()