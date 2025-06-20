
class ParkingSystemException(Exception):
    """Base exception for parking system"""
    pass

class InvalidCarIdentityException(ParkingSystemException):
    """Raised when car identity format is invalid"""
    pass

class InvalidFrequentParkingNumberException(ParkingSystemException):
    """Raised when frequent parking number is invalid"""
    pass

class CarNotFoundException(ParkingSystemException):
    """Raised when car identity is not found in parking records"""
    pass

class InvalidDateTimeException(ParkingSystemException):
    """Raised when datetime format is invalid"""
    pass

class InsufficientPaymentException(ParkingSystemException):
    """Raised when payment amount is insufficient"""
    pass

class FileOperationException(ParkingSystemException):
    """Raised when file operations fail"""
    pass
