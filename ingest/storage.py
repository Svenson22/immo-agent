import json
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from typing import Dict, Any, Set

from .config import RAW_DIR, STATE_FILE, TIMEZONE

def _today_file() -> Path:
    # Generate the file path for today's JSONL file based on the configured timezone
    tz = ZoneInfo(TIMEZONE)
    fname = datetime.now(tz).strftime("%Y-%m-%d") + ".jsonl"
    return RAW_DIR / fname

def append_jsonl(item: Dict[str, Any]) -> Path:
    # Append a JSON-encoded item as a new line to today's JSONL file
    fp = _today_file()
    with fp.open("a", encoding="utf-8") as f:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")
    return fp

def load_state() -> Dict[str, Any]:
    # Load the persistent state from the state file, or return a default state if none exists
    if STATE_FILE.exists():
        try:
            content = STATE_FILE.read_text(encoding="utf-8")
            if not content.strip():
                return {"seen_ids": []}
            return json.loads(content)
        except json.JSONDecodeError:
            return {"seen_ids": []}
    return {"seen_ids": []}

def save_state(state: Dict[str, Any]) -> None:
    # Save the given state dictionary to the state file in a pretty-printed JSON format
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

def seen_ids_set(state: Dict[str, Any]) -> Set[str]:
    # Extract the set of seen IDs from the state dictionary for quick membership checks
    return set(state.get("seen_ids", []))