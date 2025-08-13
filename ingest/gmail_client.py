from __future__ import annotations
import json
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from .config import CREDENTIALS_FILE, TOKEN_FILE, GMAIL_LABEL_NAME

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def _auth_gmail():
    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())  # type: ignore
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)
        TOKEN_FILE.write_text(creds.to_json())
    return build("gmail", "v1", credentials=creds)

def _label_id(service, label_name: str) -> Optional[str]:
    res = service.users().labels().list(userId="me").execute()
    for lbl in res.get("labels", []):
        if lbl.get("name") == label_name:
            return lbl.get("id")
    return None

def list_message_ids_with_label(service, label_name: str) -> List[str]:
    """Haalt alle messageIds op met het opgegeven label. We filteren later lokaal op 'nieuw'."""
    lbl_id = _label_id(service, label_name)
    if not lbl_id:
        raise RuntimeError(f"Gmail label '{label_name}' niet gevonden. Controleer ingest/config.py.")
    msg_ids: List[str] = []
    page_token = None
    while True:
        res = service.users().messages().list(
            userId="me",
            labelIds=[lbl_id],
            pageToken=page_token,
            maxResults=500
        ).execute()
        for msg in res.get("messages", []):
            msg_ids.append(msg["id"])
        page_token = res.get("nextPageToken")
        if not page_token:
            break
    return msg_ids

def fetch_message(service, msg_id: str) -> Dict[str, Any]:
    return service.users().messages().get(userId="me", id=msg_id, format="full").execute()

def gmail_service():
    return _auth_gmail()