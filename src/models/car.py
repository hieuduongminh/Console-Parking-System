import re
from config.settings import CAR_IDENTITY_PATTERN
from src.exceptions.parking_exceptions import InvalidCarIdentityException

class Car:
    def __init__(self, identity):
        self.identity = self._validate_identity(identity)
    
    def _validate_identity(self, identity):
        """Validate car identity format (e.g., 59C-12345)"""
        if not identity:
            raise InvalidCarIdentityException("Car identity cannot be empty")
        
        if not re.match(CAR_IDENTITY_PATTERN, identity):
            raise InvalidCarIdentityException(
                f"Invalid car identity format: {identity}. "
                "Expected format: XXX-XXXXX (e.g., 59C-12345)"
            )
        
        return identity.upper()
    
    def __str__(self):
        return self.identity
    
    def __eq__(self, other):
        if isinstance(other, Car):
            return self.identity == other.identity
        return False

