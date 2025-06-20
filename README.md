

# Console Parking System

A comprehensive parking management system built in Python that handles car parking, fee calculation, payments, and history tracking.

## Features

- **Car Parking Management**: Park and pickup cars with identity validation
- **Dynamic Pricing**: Complex pricing system based on time periods, day types, and duration
- **Frequent Parking Discounts**: Special discounts for frequent parking members
- **Credit System**: Handle overpayments as credits for future use
- **History Tracking**: Generate detailed parking history reports
- **File-based Storage**: All data persisted in JSON and text files
- **Exception Handling**: Comprehensive error handling and validation

## Project Structure

```
parking_system/
├── src/
│   ├── main.py                 # Main application
│   ├── models/                 # Data models
│   ├── services/               # Business logic
│   ├── utils/                  # Helper utilities
│   ├── exceptions/             # Custom exceptions
├── data/                       # Data storage
├── config/                     # Configuration
├── tests/                      # Unit tests
├── run.py                      # Entry point
└── README.md
```

## Installation

1. Clone or download the project
2. Navigate to the project directory
3. Run the application:

```bash
python3 run.py
```

## Usage

### 1. Park a Car
- Select option 1 from the main menu
- Enter car identity (format: XXX-XXXXX, e.g., 59C-12345)
- Enter arrival time (format: YYYY-MM-DD HH:MM)
- Optionally enter frequent parking number (5 digits with modulo 11 check digit)

### 2. Pickup a Car
- Select option 2 from the main menu
- Enter car identity
- System calculates and displays the parking fee
- Enter payment amount (must be >= required fee)
- Excess payment is stored as credits

### 3. View History
- Select option 3 from the main menu
- Enter car identity
- System generates and exports a detailed history file

## Pricing Structure

### Time Periods
- **Night (00:00-07:59)**: Flat rate of $20.00
- **Day (08:00-16:59)**: Variable rates
  - Weekday: $10.00/hour (first 8 hours), double rate for overtime
  - Weekend: Progressive rates ($10, $10, $3, $3, $3, $3, $3, $3, $2/hour)
- **Evening (17:00-23:59)**: $5.00/hour

### Frequent Parking Discounts
- **50% discount**: Night and evening periods (17:00-08:00)
- **10% discount**: Day periods (08:00-17:00)

### Overtime Policy
- Hours exceeding daily maximum are charged at double rate

## Car Identity Format
- Format: `XXX-XXXXX` (e.g., `59C-12345`, `01E-00001`)
- First two characters: digits
- Third character: letter
- Followed by hyphen and 5 digits

## Frequent Parking Number
- 5-digit number with modulo 11 check digit
- Example: `12348` (where 8 is the calculated check digit) (in assigment is 3 but I think it's wrong)

## File Storage

### Data Files
- **Parking Records**: `data/parking_records/` - Active parking sessions
- **Payment Records**: `data/payments/` - Payment history
- **Credits**: `data/credits/` - Customer credit balances
- **History**: `data/history/` - Exported history files

### File Formats
- Parking and payment data: JSON format
- History exports: Plain text format
- All datetime values: YYYY-MM-DD HH:MM format

## Error Handling

The system handles various error scenarios:
- Invalid car identity format
- Invalid frequent parking numbers
- Invalid datetime formats
- Insufficient payments
- Missing parking records
- File operation errors

## Example Usage

### Sample Test Cases

**Case 1: Regular Customer**
```
Car Identity: 50A-12345
Arrival: 2023-11-10 08:00
Departure: 2023-11-12 19:30
Frequent Parking: None
Total Fee: $347.00
```

**Case 2: Frequent Parking Customer**
```
Car Identity: 50A-12345
Arrival: 2023-11-10 08:00
Departure: 2023-11-12 19:30
Frequent Parking: 12343
Total Fee: $262.30 (with discounts applied)
```

## Development

### Adding New Features
1. Create appropriate models in `src/models/`
2. Implement business logic in `src/services/`
3. Add utility functions in `src/utils/`
4. Handle exceptions in `src/exceptions/`

### Testing
- Unit tests are located in the `tests/` directory
- Run tests using Python's unittest framework

## License

This project is for educational purposes and demonstrates:
- Object-Oriented Programming (OOP) concepts
- Exception handling
- File I/O operations
- DateTime manipulation
- Complex business logic implementation
- Modular code organization

#===============================================================================




