import json
import os
from pathlib import Path
from config.settings import *
from exceptions.parking_exceptions import FileOperationException

class FileHandler:
    @staticmethod
    def save_parking_record(car_identity, record_data):
        """Save parking record to file"""
        try:
            filename = PARKING_RECORDS_DIR / f"{car_identity.replace('-', '_')}.json"
            with open(filename, 'w') as f:
                json.dump(record_data, f, indent=2)
        except Exception as e:
            raise FileOperationException(f"Failed to save parking record: {e}")
    
    @staticmethod
    def load_parking_record(car_identity):
        """Load parking record from file"""
        try:
            filename = PARKING_RECORDS_DIR / f"{car_identity.replace('-', '_')}.json"
            if not filename.exists():
                return None
            
            with open(filename, 'r') as f:
                return json.load(f)
        except Exception as e:
            raise FileOperationException(f"Failed to load parking record: {e}")
    
    @staticmethod
    def delete_parking_record(car_identity):
        """Delete parking record file"""
        try:
            filename = PARKING_RECORDS_DIR / f"{car_identity.replace('-', '_')}.json"
            if filename.exists():
                filename.unlink()
        except Exception as e:
            raise FileOperationException(f"Failed to delete parking record: {e}")
    
    @staticmethod
    def save_payment_record(car_identity, payment_data):
        """Save payment record"""
        try:
            filename = PAYMENTS_DIR / f"{car_identity.replace('-', '_')}_payments.json"
            
            # Load existing payments or create new list
            payments = []
            if filename.exists():
                with open(filename, 'r') as f:
                    payments = json.load(f)
            
            payments.append(payment_data)
            
            with open(filename, 'w') as f:
                json.dump(payments, f, indent=2)
        except Exception as e:
            raise FileOperationException(f"Failed to save payment record: {e}")
    
    @staticmethod
    def load_payment_records(car_identity):
        """Load all payment records for a car"""
        try:
            filename = PAYMENTS_DIR / f"{car_identity.replace('-', '_')}_payments.json"
            if not filename.exists():
                return []
            
            with open(filename, 'r') as f:
                return json.load(f)
        except Exception as e:
            raise FileOperationException(f"Failed to load payment records: {e}")
    
    @staticmethod
    def save_credit_balance(car_identity, credit_amount):
        """Save customer credit balance"""
        try:
            filename = CREDITS_DIR / f"{car_identity.replace('-', '_')}_credits.json"
            credit_data = {
                'car_identity': car_identity,
                'credit_balance': credit_amount
            }
            
            with open(filename, 'w') as f:
                json.dump(credit_data, f, indent=2)
        except Exception as e:
            raise FileOperationException(f"Failed to save credit balance: {e}")
    
    @staticmethod
    def load_credit_balance(car_identity):
        """Load customer credit balance"""
        try:
            filename = CREDITS_DIR / f"{car_identity.replace('-', '_')}_credits.json"
            if not filename.exists():
                return 0.0
            
            with open(filename, 'r') as f:
                credit_data = json.load(f)
                return credit_data.get('credit_balance', 0.0)
        except Exception as e:
            raise FileOperationException(f"Failed to load credit balance: {e}")
    
    @staticmethod
    def export_history_file(car_identity, history_content):
        """Export history file"""
        try:
            filename = HISTORY_DIR / f"{car_identity}.txt"
            with open(filename, 'w') as f:
                f.write(history_content)
            return str(filename)
        except Exception as e:
            raise FileOperationException(f"Failed to export history file: {e}")
