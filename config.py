from pathlib import Path

# ---------------------------------------
# IB SETTINGS
# ---------------------------------------

IB_HOST = "127.0.0.1"
IB_PORT = 7497
CLIENT_ID = 1

# ---------------------------------------
# DATA REQUEST SETTINGS
# ---------------------------------------

BAR_SIZE_DEFAULT = "1 day"
DURATION_DEFAULT = "1 Y"
WHAT_TO_SHOW = "TRADES"
USE_RTH = True
FORMAT_DATE = 1

TIMEFRAMES = {
    "1min": {
        "bar_size": "1 min",
        "duration": "2 D",
        "max_requests": 50,
    },
    "5min": {
        "bar_size": "5 mins",
        "duration": "5 D",
        "max_requests": 200,
    },
    "1h": {
        "bar_size": "1 hour",
        "duration": "1 M",
        "max_requests": 500,
    },
    "1day": {
        "bar_size": "1 day",
        "duration": "1 Y",
        "max_requests": None,  
    },
}


# ---------------------------------------
# PROJECT PATHS
# ---------------------------------------

ROOT = Path(__file__).resolve().parent
DATA_ROOT = ROOT / "historical_data"

