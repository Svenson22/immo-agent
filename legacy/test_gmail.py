#!/usr/bin/env python3
import sys
from pathlib import Path

# Ensure project root is in sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from ingest.gmail_client import gmail_service, list_message_ids_with_label

# Note: label name is explicitly set and case-sensitive!
GMAIL_LABEL_NAME = "immo-agent"

if __name__ == "__main__":
    svc = gmail_service()
    print("✅ Gmail API verbonden!")

    # Retrieve all labels
    res = svc.users().labels().list(userId='me').execute()
    labels = res.get('labels', [])
    label_names = [lbl.get('name') for lbl in labels]

    print(f"Labels gevonden: {len(label_names)}")
    for name in sorted(label_names):
        print("-", name)

    # Check if ingest label exists
    target = GMAIL_LABEL_NAME
    print(f"\nSearch for label: '{target}'")
    if target in label_names:
        print("[OK] Label exists.")
        try:
            ids = list_message_ids_with_label(svc, target)
            print(f"Number of messages with '{target}': {len(ids)}")
            if ids:
                print("Example IDs:", ids[:5])
        except Exception as e:
            print("[warn] Could not retrieve messages:", e)
    else:
        print("[MISS] Label not found. Check the exact name in Gmail (case-sensitive).")
