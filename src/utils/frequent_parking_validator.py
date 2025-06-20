
def validate_frequent_parking_number(number_str):
    """
    Validate frequent parking number using modulo 11 check digit calculation
    Format: 4 digits + 1 check digit (e.g., 12348, 11113)
    """
    if not number_str or len(number_str) != 5:
        return False
    
    if not number_str.isdigit():
        return False
    
    # Extract the first 4 digits and the check digit
    digits = number_str[:4]
    check_digit = int(number_str[4])
    
    # Calculate modulo 11 check digit
    weighted_sum = 0
    weights = [5, 4, 3, 2]  # Weights for positions 1-4
    
    for i, digit in enumerate(digits):
        weighted_sum += int(digit) * weights[i]
    
    calculated_check_digit = weighted_sum % 11
    
    # Handle special cases for modulo 11
    if calculated_check_digit == 10:
        calculated_check_digit = 0
    
    return calculated_check_digit == check_digit
