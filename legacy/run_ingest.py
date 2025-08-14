#!/usr/bin/env python
from ingest.gmail_client import gmail_service, list_message_ids_with_label, fetch_message
from ingest.extract import parse_message
from ingest.storage import append_jsonl, load_state, save_state, seen_ids_set
from ingest.config import GMAIL_LABEL_NAME

import argparse
import json

def main(dry_run: bool = False):
    print(f"[ingest] Start – label='{GMAIL_LABEL_NAME}'")
    svc = gmail_service()
    msg_ids = list_message_ids_with_label(svc, GMAIL_LABEL_NAME)
    print(f"[ingest] Found messages with label: {len(msg_ids)}")

    state = load_state()
    already = seen_ids_set(state)
    new_ids = [m for m in msg_ids if m not in already]
    if not new_ids:
        print("[ingest] No new messages. Done.")
        return

    print(f"[ingest] New messages to process: {len(new_ids)}")
    if dry_run:
        print("[ingest] DRY-RUN is ON → will NOT write files or update state.")

    processed = 0
    for mid in new_ids:
        msg = fetch_message(svc, mid)
        item = parse_message(msg)
        if dry_run:
            # Show a compact preview for debugging
            preview = {
                "message_id": item.get("message_id"),
                "subject": item.get("subject"),
                "prices": item.get("prices", [])[:3],
                "links": item.get("links", [])[:3],
            }
            print("[preview]", json.dumps(preview, ensure_ascii=False))
        else:
            out_file = append_jsonl(item)
            state.setdefault("seen_ids", []).append(mid)
        processed += 1

    if dry_run:
        print(f"[ingest] DRY-RUN complete. Parsed: {processed} messages. State not updated; no files written.")
    else:
        save_state(state)
        print(f"[ingest] Processed: {processed} → output in {out_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest labeled Gmail messages into daily raw JSONL batches.")
    parser.add_argument("--dry-run", action="store_true", help="Parse and preview items without writing files or updating state")
    args = parser.parse_args()
    main(dry_run=args.dry_run)