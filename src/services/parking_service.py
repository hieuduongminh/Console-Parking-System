from datetime import datetime

from src.models.parking_record import ParkingRecord
from src.services.validation_service import ValidationService
from src.services.pricing_service import PricingService
from src.utils.file_handler import FileHandler
from src.exceptions.parking_exceptions import *

class ParkingService:
    def __init__(self):
        self.file_handler = FileHandler()
        self.validation_service = ValidationService()
        self.pricing_service = PricingService()
    
    def park_car(self, car_identity_str, arrival_time_str, frequent_parking_str=None):
        """Park a car - store parking record"""
        try:
            # Validate inputs
            car = self.validation_service.validate_car_identity(car_identity_str)
            arrival_time = self.validation_service.validate_datetime(arrival_time_str)
            frequent_parking_number = self.validation_service.validate_frequent_parking_number(frequent_parking_str)
            
            # Check if car is already parked
            existing_record = self.file_handler.load_parking_record(car.identity)
            if existing_record and not existing_record.get('departure_time'):
                raise ParkingSystemException(f"Car {car.identity} is already parked")
            
            # Create parking record
            parking_record = ParkingRecord(car.identity, arrival_time, frequent_parking_number)
            
            # Save to file
            self.file_handler.save_parking_record(car.identity, parking_record.to_dict())
            
            return f"Car {car.identity} parked successfully at {arrival_time_str}"
        
        except (InvalidCarIdentityException, InvalidFrequentParkingNumberException, 
                InvalidDateTimeException, ParkingSystemException) as e:
            raise e
        except Exception as e:
            raise ParkingSystemException(f"Failed to park car: {e}")
    
    def pickup_car(self, car_identity_str, payment_amount_str):
        """Pickup a car - calculate fee and process payment"""
        try:
            # Validate car identity
            car = self.validation_service.validate_car_identity(car_identity_str)
            
            # Load parking record
            record_data = self.file_handler.load_parking_record(car.identity)
            if not record_data:
                raise CarNotFoundException(f"No parking record found for car {car.identity}")
            
            parking_record = ParkingRecord.from_dict(record_data)
            
            if parking_record.departure_time:
                raise ParkingSystemException(f"Car {car.identity} has already been picked up")
            
            # Calculate fee
            departure_time = datetime.now()
            has_frequent_parking = parking_record.frequent_parking_number is not None
            
            total_fee, calculation_details = self.pricing_service.calculate_parking_fee(
                parking_record.arrival_time,
                departure_time,
                has_frequent_parking
            )
            
            # Load existing credits
            existing_credits = self.file_handler.load_credit_balance(car.identity)
            
            # Apply credits to reduce fee
            fee_after_credits = max(0, total_fee - existing_credits)
            credits_used = min(existing_credits, total_fee)
            
            # Validate payment
            payment_amount = self.validation_service.validate_payment_amount(
                payment_amount_str, fee_after_credits
            )
            
            # Calculate new credits
            new_credits = existing_credits - credits_used + (payment_amount - fee_after_credits)
            
            # Update parking record
            parking_record.set_departure(departure_time, total_fee)
            parking_record.set_payment(payment_amount)
            
            # Save records
            self.file_handler.save_parking_record(car.identity, parking_record.to_dict())
            self.file_handler.save_payment_record(car.identity, {
                'arrival_time': parking_record.to_dict()['arrival_time'],
                'departure_time': parking_record.to_dict()['departure_time'],
                'total_fee': total_fee,
                'payment_amount': payment_amount,
                'credits_used': credits_used,
                'timestamp': datetime.now().isoformat()
            })
            self.file_handler.save_credit_balance(car.identity, new_credits)
            
            # Delete active parking record
            self.file_handler.delete_parking_record(car.identity)
            
            return {
                'car_identity': car.identity,
                'total_fee': total_fee,
                'credits_used': credits_used,
                'fee_after_credits': fee_after_credits,
                'payment_amount': payment_amount,
                'new_credits': new_credits,
                'calculation_details': calculation_details
            }
        
        except (InvalidCarIdentityException, CarNotFoundException, 
                InsufficientPaymentException, ParkingSystemException) as e:
            raise e
        except Exception as e:
            raise ParkingSystemException(f"Failed to pickup car: {e}")
    
    def generate_history(self, car_identity_str):
        """Generate parking history for a car"""
        try:
            # Validate car identity
            car = self.validation_service.validate_car_identity(car_identity_str)
            
            # Load payment records
            payment_records = self.file_handler.load_payment_records(car.identity)
            credit_balance = self.file_handler.load_credit_balance(car.identity)
            
            if not payment_records:
                raise CarNotFoundException(f"No parking history found for car {car.identity}")
            
            # Calculate totals
            total_payments = sum(record['payment_amount'] for record in payment_records)
            
            # Generate history content
            history_content = f"Total payment: ${total_payments:.2f}\n"
            history_content += f"Available credits: ${credit_balance:.2f}\n"
            history_content += "Parked Dates:\n"
            
            for record in payment_records:
                arrival = record['arrival_time']
                departure = record['departure_time']
                fee = record['total_fee']
                history_content += f"{arrival} – {departure} ${fee:.2f}\n"
            
            # Export to file
            filename = self.file_handler.export_history_file(car.identity, history_content)
            
            return {
                'filename': filename,
                'content': history_content,
                'total_payments': total_payments,
                'available_credits': credit_balance,
                'records_count': len(payment_records)
            }
        
        except (InvalidCarIdentityException, CarNotFoundException) as e:
            raise e
        except Exception as e:
            raise ParkingSystemException(f"Failed to generate history: {e}")
