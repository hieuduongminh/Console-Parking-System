import unittest
import sys
import os

# Add the parent directory to the path so Python can find the src module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.utils.frequent_parking_validator import validate_frequent_parking_number

class TestFrequentParkingValidator(unittest.TestCase):
    def test_valid_frequent_parking_numbers(self):
        """Test valid frequent parking numbers"""
        # Manual calculation for 1234:
        # 1*5 + 2*4 + 3*3 + 4*2 = 5 + 8 + 9 + 8 = 30
        # 30 % 11 = 8
        # So 12348 should be valid
        self.assertTrue(validate_frequent_parking_number("12348"))
        
        # Additional test cases
        valid_numbers = ["12348", "11113", "22226"]
        
        for number in valid_numbers:
            self.assertTrue(validate_frequent_parking_number(number))
    
    def test_invalid_frequent_parking_numbers(self):
        """Test invalid frequent parking numbers"""
        invalid_numbers = [
            "",
            "1234",      # Too short
            "123456",    # Too long
            "abcde",     # Non-numeric
            "12345",     # Wrong check digit
            "12340",     # Wrong check digit
        ]
        
        for number in invalid_numbers:
            self.assertFalse(validate_frequent_parking_number(number))

if __name__ == '__main__':
    unittest.main()