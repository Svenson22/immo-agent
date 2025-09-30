# scripts/test_gmail.py
from __future__ import annotations
import os
import pathlib
import pickle  # alleen als je later pickle wil gebruiken
from typing import Optional

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Alleen leesrechten is voldoende voor ophalen mails
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

ROOT = pathlib.Path(__file__).resolve().parents[1]
CFG_DIR = ROOT / "config"
TOKEN_PATH = CFG_DIR / "token.json"
CREDS_PATH = CFG_DIR / "credentials.json"

def get_credentials() -> Credentials:
    creds: Optional[Credentials] = None

    # 1) Bestaande token gebruiken als die er is
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)

    # 2) Zo niet: OAuth-flow starten in browser en token wegschrijven
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Probeer te refreshen
            try:
                creds.refresh(Request())  # type: ignore[name-defined]
            except Exception:
                creds = None  # fallback naar flow
        if not creds:
            assert CREDS_PATH.exists(), f"credentials.json niet gevonden op: {CREDS_PATH}"
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDS_PATH), SCOPES)
            # Gebruik lokale server flow (opent browser)
            creds = flow.run_local_server(port=0)
        # Schrijf/overschrijf token
        TOKEN_PATH.write_text(creds.to_json())

    return creds

def main():
    creds = get_credentials()
    service = build("gmail", "v1", credentials=creds)

    # Eenvoudige test: labels ophalen en printen
    results = service.users().labels().list(userId="me").execute()
    labels = results.get("labels", [])
    print("\n✅ Verbinding gelukt. Aantal labels:", len(labels))
    for lb in labels[:10]:
        print("-", lb.get("name"))
    if len(labels) > 10:
        print("...")

if __name__ == "__main__":
    main()