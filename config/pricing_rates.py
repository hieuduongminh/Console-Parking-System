
# Pricing rates by time period and day type
PRICING_RATES = {
    # Weekdays (Monday-Friday)
    'weekday': {
        '00:00-07:59': 20.00,  # Night rate (flat rate)
        '08:00-16:59': 10.00,  # Day rate (per hour)
        '17:00-23:59': 5.00,   # Evening rate (per hour)
    },
    # Saturday
    'saturday': {
        '00:00-07:59': 20.00,  # Night rate (flat rate)
        '08:00-16:59': 3.00,   # Day rate (per hour) - Weekend discount
        '17:00-23:59': 5.00,   # Evening rate (per hour)
    },
    # Sunday
    'sunday': {
        '00:00-07:59': 20.00,  # Night rate (flat rate)
        '08:00-16:59': 2.00,   # Day rate (per hour) - Weekend discount
        '17:00-23:59': 5.00,   # Evening rate (per hour)
    }, 
}

# Frequent parking discounts
FREQUENT_PARKING_DISCOUNTS = {
    'night_early': 0.5,  # 50% discount for 17:00-Midnight, Midnight-08:00
    'other': 0.1,        # 10% discount for other times
}
