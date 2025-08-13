# ingest/config.py
import os
from pathlib import Path

# Labelnaam voor Gmail-filter
GMAIL_LABEL_NAME = os.getenv("IMMO_GMAIL_LABEL", "ImmoAgent")

# Tijdzone voor datum/tijd-stempels
TIMEZONE = os.getenv("IMMO_TZ", "Europe/Brussels")

# Basisstructuur paden
REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = REPO_ROOT / "config"
DATA_DIR = REPO_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
STATE_FILE = DATA_DIR / "state.json"

# Mappen aanmaken als ze nog niet bestaan
CONFIG_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)
RAW_DIR.mkdir(parents=True, exist_ok=True)

# Gmail OAuth-bestanden
CREDENTIALS_FILE = CONFIG_DIR / "credentials.json"  # OAuth client ID van Google
TOKEN_FILE = CONFIG_DIR / "token.json"              # Wordt aangemaakt na eerste login