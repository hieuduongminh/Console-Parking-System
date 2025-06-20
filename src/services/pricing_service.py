from config.pricing_rates import *
from src.utils.datetime_helper import calculate_duration_by_periods
import math

class PricingService:
    @staticmethod
    def calculate_parking_fee(arrival_time, departure_time, has_frequent_parking=False):
        """
        Calculate total parking fee based on arrival and departure times
        """
        if departure_time <= arrival_time:
            raise ValueError("Departure time must be after arrival time")
        
        # Get duration breakdown by periods
        duration_breakdown = calculate_duration_by_periods(arrival_time, departure_time)
        
        total_fee = 0.0
        calculation_details = []


        # Process each period in the duration breakdown
        for date, day_type, period, hours, flag in duration_breakdown:
            
            # Round up hours to the nearest hour
            hours = math.ceil(hours)
            
            period_fee = PricingService._calculate_period_fee(
                date, day_type, period, hours, has_frequent_parking, flag
            )
            
            # Append to calculation details
            calculation_details.append({
                'date': date,
                'day_type': day_type,
                'period': period,
                'hours': hours,
                'fee': period_fee,
                'flag': flag,
                'has_frequent_parking': has_frequent_parking
            })
            total_fee += period_fee
        
        return round(total_fee, 2), calculation_details
    
    @staticmethod
    def _calculate_period_fee(date, day_type, period, hours, has_frequent_parking, flag):
        """Calculate fee for a specific period"""
        # Get base fee from pricing rates
        base_fee = PRICING_RATES[day_type][period]

        # Determine if this is an early morning period (flat rate)
        if period == '00:00-07:59':
            if has_frequent_parking is True:
                # Apply frequent parking discount for early morning
                base_fee *= (1 - FREQUENT_PARKING_DISCOUNTS['night_early'])

            return base_fee
            
        # Apply overtime multiplier if needed
        if flag == 'exceed_time':
            base_fee *= 2
            
        # Apply frequent parking discount if applicable
        if has_frequent_parking:

            if period == '17:00-23:59':
                # Apply frequent parking discount for evening period
                base_fee *= (1 - FREQUENT_PARKING_DISCOUNTS['night_early'])
            else:
                base_fee *= (1 - FREQUENT_PARKING_DISCOUNTS['other'])
            
        # Multiply by hours (for non-flat rate periods)
        return base_fee * hours
