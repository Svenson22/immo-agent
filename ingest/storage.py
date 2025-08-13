import json
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from typing import Dict, Any, Set

from .config import RAW_DIR, STATE_FILE, TIMEZONE

def _today_file() -> Path:
    tz = ZoneInfo(TIMEZONE)
    fname = datetime.now(tz).strftime("%Y-%m-%d") + ".jsonl"
    return RAW_DIR / fname

def append_jsonl(item: Dict[str, Any]) -> Path:
    fp = _today_file()
    with fp.open("a", encoding="utf-8") as f:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")
    return fp

def load_state() -> Dict[str, Any]:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {"seen_ids": []}

def save_state(state: Dict[str, Any]) -> None:
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

def seen_ids_set(state: Dict[str, Any]) -> Set[str]:
    return set(state.get("seen_ids", []))