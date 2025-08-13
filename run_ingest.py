#!/usr/bin/env python
from ingest.gmail_client import gmail_service, list_message_ids_with_label, fetch_message
from ingest.extract import parse_message
from ingest.storage import append_jsonl, load_state, save_state, seen_ids_set
from ingest.config import GMAIL_LABEL_NAME

def main():
    print(f"[ingest] Start – label='{GMAIL_LABEL_NAME}'")
    svc = gmail_service()
    msg_ids = list_message_ids_with_label(svc, GMAIL_LABEL_NAME)
    print(f"[ingest] Gevonden berichten met label: {len(msg_ids)}")

    state = load_state()
    already = seen_ids_set(state)
    new_ids = [m for m in msg_ids if m not in already]
    if not new_ids:
        print("[ingest] Geen nieuwe berichten. Klaar.")
        return

    print(f"[ingest] Nieuwe berichten te verwerken: {len(new_ids)}")
    processed = 0
    for mid in new_ids:
        msg = fetch_message(svc, mid)
        item = parse_message(msg)
        out_file = append_jsonl(item)
        processed += 1
        state.setdefault("seen_ids", []).append(mid)

    save_state(state)
    print(f"[ingest] Verwerkt: {processed} → output in {out_file}")

if __name__ == "__main__":
    main()