# ingest/config.py
import os
from pathlib import Path

# Label name for Gmail filter
GMAIL_LABEL_NAME = os.getenv("IMMO_GMAIL_LABEL", "immo-agent")

# Timezone for date/time stamps
TIMEZONE = os.getenv("IMMO_TZ", "Europe/Brussels")

# Base directory structure
REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = REPO_ROOT / "config"
DATA_DIR = REPO_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
STATE_FILE = DATA_DIR / "state.json"

# Create directories if they do not exist
CONFIG_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)
RAW_DIR.mkdir(parents=True, exist_ok=True)

# Gmail OAuth files
CREDENTIALS_FILE = CONFIG_DIR / "credentials.json"  # Google OAuth client ID
TOKEN_FILE = CONFIG_DIR / "token.json"              # Created after first login