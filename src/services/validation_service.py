from src.models.car import Car
from src.utils.frequent_parking_validator import validate_frequent_parking_number
from src.utils.datetime_helper import parse_datetime
from src.exceptions.parking_exceptions import *

class ValidationService:
    @staticmethod
    def validate_car_identity(identity):
        """Validate and return Car object"""
        try:
            return Car(identity)
        except InvalidCarIdentityException:
            raise
    
    @staticmethod
    def validate_frequent_parking_number(number_str):
        """Validate frequent parking number"""
        if not number_str or number_str.strip() == '':
            return None
        
        number_str = number_str.strip()
        if not validate_frequent_parking_number(number_str):
            raise InvalidFrequentParkingNumberException(
                f"Invalid frequent parking number: {number_str}. "
                "Must be 4 digits + 1 check digit calculated using modulo 11. e.g., 12348"
            )
        
        return number_str
    
    @staticmethod
    def validate_datetime(datetime_str):
        """Validate datetime string"""
        try:
            return parse_datetime(datetime_str)
        except InvalidDateTimeException:
            raise
    
    @staticmethod
    def validate_payment_amount(amount_str, required_amount):
        """Validate payment amount"""
        try:
            amount = float(amount_str)
            if amount < 0:
                raise ValueError("Payment amount cannot be negative")
            
            if amount < required_amount:
                raise InsufficientPaymentException(
                    f"Insufficient payment. Required: ${required_amount:.2f}, Provided: ${amount:.2f}"
                )
            
            return amount
        except ValueError as e:
            if "Insufficient payment" in str(e):
                raise
            raise ValueError(f"Invalid payment amount: {amount_str}")
