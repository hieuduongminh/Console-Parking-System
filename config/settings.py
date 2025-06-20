from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
PARKING_RECORDS_DIR = DATA_DIR / "parking_records"
PAYMENTS_DIR = DATA_DIR / "payments"
CREDITS_DIR = DATA_DIR / "credits"
HISTORY_DIR = DATA_DIR / "history"

# Create directories if they don't exist
for directory in [DATA_DIR, PARKING_RECORDS_DIR, PAYMENTS_DIR, CREDITS_DIR, HISTORY_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# File formats
DATE_FORMAT = "%Y-%m-%d %H:%M"
CURRENCY_FORMAT = "{:.2f}"

# Car identity pattern
CAR_IDENTITY_PATTERN = r'^[0-9]{2}[A-Z]-[0-9]{5}$'
