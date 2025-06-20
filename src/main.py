import sys
from datetime import datetime

from services.parking_service import ParkingService
from exceptions.parking_exceptions import *
from utils.file_handler import FileHandler
from models.parking_record import ParkingRecord
from services.pricing_service import PricingService

class ParkingSystemApp:
    def __init__(self):
        self.parking_service = ParkingService()
    
    def display_menu(self):
        """Display main menu options"""
        print("\n" + "="*50)
        print("        CONSOLE PARKING SYSTEM")
        print("="*50)
        print("1. Park Car (IN)")
        print("2. Pickup Car (OUT)")
        print("3. View History")
        print("4. Exit")
        print("="*50)
    
    def get_user_choice(self):
        """Get user menu choice"""
        while True:
            try:
                choice = input("Please select an option (1-4): ").strip()
                if choice in ['1', '2', '3', '4']:
                    return choice
                else:
                    print("Invalid choice. Please select 1, 2, 3, or 4.")
            except KeyboardInterrupt:
                print("\nExiting...")
                sys.exit(0)
    
    def handle_park_car(self):
        """Handle park car option"""
        print("\n--- PARK CAR ---")
        try:
            car_identity = input("Enter car identity (e.g., 59C-12345): ").strip()
            arrival_time = input("Enter arrival time (YYYY-MM-DD HH:MM): ").strip()
            frequent_parking = input("Enter frequent parking number (optional, press Enter to skip): ").strip()
            
            if not frequent_parking:
                frequent_parking = None
            
            result = self.parking_service.park_car(car_identity, arrival_time, frequent_parking)
            print(f"\n✓ {result}")
            
        except (InvalidCarIdentityException, InvalidFrequentParkingNumberException, 
                InvalidDateTimeException, ParkingSystemException) as e:
            print(f"\n✗ Error: {e}")
        except Exception as e:
            print(f"\n✗ Unexpected error: {e}")
    
    def handle_pickup_car(self):
        """Handle pickup car option"""
        print("\n--- PICKUP CAR ---")
        try:
            car_identity = input("Enter car identity: ").strip()
            
            # First, let's show the calculated fee
            try:
                # We need to calculate the fee first to show to user
                file_handler = FileHandler()
                record_data = file_handler.load_parking_record(car_identity)
                
                if not record_data:
                    raise CarNotFoundException(f"No parking record found for car {car_identity}")
                
                parking_record = ParkingRecord.from_dict(record_data)
                departure_time = datetime.now()
                has_frequent_parking = parking_record.frequent_parking_number is not None
                
                pricing_service = PricingService()
                total_fee, calculation_details = pricing_service.calculate_parking_fee(
                    parking_record.arrival_time,
                    departure_time,
                    has_frequent_parking
                )
                
                # Show existing credits
                existing_credits = file_handler.load_credit_balance(car_identity)
                fee_after_credits = max(0, total_fee - existing_credits)
                
                print(f"\n--- PARKING CALCULATION ---")
                print(f"Car Identity: {car_identity}")
                print(f"Arrival Time: {parking_record.arrival_time}")
                print(f"Departure Time: {departure_time}")
                print(f"Total Parking Fee: ${total_fee:.2f}")
                if existing_credits > 0:
                    print(f"Available Credits: ${existing_credits:.2f}")
                    print(f"Fee After Credits: ${fee_after_credits:.2f}")
                
                print(f"\nAmount to Pay: ${fee_after_credits:.2f}")
                
            except Exception as e:
                print(f"Error calculating fee: {e}")
                return
            
            payment_amount = input(f"Enter payment amount (minimum ${fee_after_credits:.2f}): $").strip()
            
            result = self.parking_service.pickup_car(car_identity, payment_amount)
            
            print(f"\n--- PICKUP SUCCESSFUL ---")
            print(f"Car Identity: {result['car_identity']}")
            print(f"Total Fee: ${result['total_fee']:.2f}")
            if result['credits_used'] > 0:
                print(f"Credits Used: ${result['credits_used']:.2f}")
            print(f"Payment Amount: ${result['payment_amount']:.2f}")
            if result['new_credits'] > 0:
                print(f"New Credit Balance: ${result['new_credits']:.2f}")
            
        except (InvalidCarIdentityException, CarNotFoundException, 
                InsufficientPaymentException, ParkingSystemException) as e:
            print(f"\n✗ Error: {e}")
        except Exception as e:
            print(f"\n✗ Unexpected error: {e}")
    
    def handle_view_history(self):
        """Handle view history option"""
        print("\n--- VIEW HISTORY ---")
        try:
            car_identity = input("Enter car identity: ").strip()
            
            result = self.parking_service.generate_history(car_identity)
            
            print(f"\n--- PARKING HISTORY FOR {car_identity} ---")
            print(result['content'])
            print(f"History exported to: {result['filename']}")
            print(f"Total Records: {result['records_count']}")
            
        except (InvalidCarIdentityException, CarNotFoundException) as e:
            print(f"\n✗ Error: {e}")
        except Exception as e:
            print(f"\n✗ Unexpected error: {e}")
    
    def run(self):
        """Main application loop"""
        print("Welcome to Console Parking System!")
        
        while True:
            try:
                self.display_menu()
                choice = self.get_user_choice()
                
                if choice == '1':
                    self.handle_park_car()
                elif choice == '2':
                    self.handle_pickup_car()
                elif choice == '3':
                    self.handle_view_history()
                elif choice == '4':
                    print("\nThank you for using Console Parking System!")
                    break
                
                input("\nPress Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n\nExiting...")
                break
            except Exception as e:
                print(f"\nUnexpected error: {e}")
                input("Press Enter to continue...")

def main():
    """Application entry point"""
    try:
        app = ParkingSystemApp()
        app.run()
    except Exception as e:
        print(f"Failed to start application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
