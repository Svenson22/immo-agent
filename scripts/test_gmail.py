import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

#!/usr/bin/env python3
from ingest.gmail_client import gmail_service as authenticate_gmail

if __name__ == "__main__":
    svc = authenticate_gmail()
    print("✅ Gmail API verbonden!")
    # Optioneel: toon 5 labels, zodat je meteen ziet dat het werkt
    labels = svc.users().labels().list(userId="me").execute().get("labels", [])
    for lbl in labels[:5]:
        print("-", lbl.get("name"))
