
import unittest
import sys
import os

# Add the parent directory to the path so Python can find the src module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.models.car import Car
from src.exceptions.parking_exceptions import InvalidCarIdentityException



class TestCar(unittest.TestCase):
    def test_valid_car_identity(self):
        """Test valid car identity formats"""
        valid_identities = ["59C-12345", "01E-00001", "99Z-99999"]
        
        for identity in valid_identities:
            car = Car(identity)
            self.assertEqual(car.identity, identity.upper())
    
    def test_invalid_car_identity(self):
        """Test invalid car identity formats"""
        invalid_identities = [
            "",
            "59C12345",     # Missing hyphen
            "59-12345",     # Missing letter
            "59CC-12345",   # Too many letters
            "5C-12345",     # Too few digits at start
            "59C-1234",     # Too few digits at end
            "59C-123456",   # Too many digits at end
            "abc-12345",    # Invalid format
        ]
        
        for identity in invalid_identities:
            with self.assertRaises(InvalidCarIdentityException):
                Car(identity)
    
    def test_car_equality(self):
        """Test car equality comparison"""
        car1 = Car("59C-12345")
        car3 = Car("01E-00001")

        self.assertNotEqual(car1, car3)  # Should not be equal


if __name__ == '__main__':
    unittest.main()
