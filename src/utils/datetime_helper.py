from datetime import datetime, timedelta

from config.settings import DATE_FORMAT
from src.exceptions.parking_exceptions import InvalidDateTimeException

def parse_datetime(datetime_str):
    """Parse datetime string to datetime object"""
    try:
        return datetime.strptime(datetime_str, DATE_FORMAT)
    except ValueError:
        raise InvalidDateTimeException(f"Invalid datetime format: {datetime_str}. Expected format: YYYY-MM-DD HH:MM")

def format_datetime(dt):
    """Format datetime object to string"""
    return dt.strftime(DATE_FORMAT)

import calendar

def get_day_type(dt):
    """Determine the type of day for a given datetime."""
    day_types = {
        calendar.SATURDAY: 'saturday',
        calendar.SUNDAY: 'sunday'
    }
    return day_types.get(dt.weekday(), 'weekday')

def get_time_period(dt):
    """Get time period for pricing (00:00-07:59, 08:00-16:59, 17:00-23:59)"""
    hour = dt.hour
    if 0 <= hour < 8:
        return '00:00-07:59'
    elif 8 <= hour < 17:
        return '08:00-16:59'
    else:
        return '17:00-23:59'
    
    
def calculate_duration_by_periods(start_dt, end_dt):
    """
    Calculate parking duration broken down by time periods and days
    Returns list of (date, day_type, period, hours) tuples
    """
    duration_breakdown = []
    current_dt = start_dt
    
    # Define period boundaries
    period_boundaries = {
        '00:00-07:59': lambda dt: dt.replace(hour=8, minute=0, second=0, microsecond=0),
        '08:00-16:59': lambda dt: dt.replace(hour=17, minute=0, second=0, microsecond=0),
        '17:00-23:59': lambda dt: (dt.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1))
    }
    
    # Define time limits for different day types and periods
    time_limits = {
        ('weekday', '08:00-16:59'): 2,
        ('saturday', '08:00-16:59'): 4,
        ('sunday', '08:00-16:59'): 8
    }
    
    while current_dt < end_dt:
        current_date = current_dt.date()
        day_type = get_day_type(current_dt)
        current_period = get_time_period(current_dt)
        
        # Calculate end of current period
        period_end = period_boundaries[current_period](current_dt)
        actual_period_end = min(period_end, end_dt)
        
        hours_in_period = (actual_period_end - current_dt).total_seconds() / 3600
        
        # Check if this is a period with a time limit
        time_limit = time_limits.get((day_type, current_period))
        
        if time_limit and hours_in_period > time_limit:
            # Add entry for the limited hours
            duration_breakdown.append((
                current_date,
                day_type,
                current_period,
                time_limit,
                "normal"
            ))
            # Add entry for excess hours
            duration_breakdown.append((
                current_date,
                day_type,
                current_period,
                hours_in_period - time_limit,
                "exceed_time"
            ))
        else:
            # Normal entry
            duration_breakdown.append((
                current_date,
                day_type,
                current_period,
                hours_in_period,
                "normal"
            ))

        current_dt = actual_period_end
    
    return duration_breakdown
