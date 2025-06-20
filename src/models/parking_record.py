
from datetime import datetime
from utils.datetime_helper import parse_datetime, format_datetime

class ParkingRecord:
    def __init__(self, car_identity, arrival_time, frequent_parking_number=None):
        self.car_identity = car_identity
        self.arrival_time = arrival_time if isinstance(arrival_time, datetime) else parse_datetime(arrival_time)
        self.frequent_parking_number = frequent_parking_number
        self.departure_time = None
        self.total_fee = None
        self.payment_amount = None
        self.created_at = datetime.now()
    
    def set_departure(self, departure_time, total_fee):
        """Set departure time and calculated fee"""
        self.departure_time = departure_time if isinstance(departure_time, datetime) else parse_datetime(departure_time)
        self.total_fee = total_fee
    
    def set_payment(self, payment_amount):
        """Set payment amount"""
        self.payment_amount = payment_amount
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'car_identity': self.car_identity,
            'arrival_time': format_datetime(self.arrival_time),
            'departure_time': format_datetime(self.departure_time) if self.departure_time else None,
            'frequent_parking_number': self.frequent_parking_number,
            'total_fee': self.total_fee,
            'payment_amount': self.payment_amount,
            'created_at': format_datetime(self.created_at)
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create ParkingRecord from dictionary"""
        record = cls(
            data['car_identity'],
            data['arrival_time'],
            data.get('frequent_parking_number')
        )
        
        if data.get('departure_time'):
            record.departure_time = parse_datetime(data['departure_time'])
        
        record.total_fee = data.get('total_fee')
        record.payment_amount = data.get('payment_amount')
        record.created_at = parse_datetime(data['created_at'])
        
        return record
