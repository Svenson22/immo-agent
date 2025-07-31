from gmail_auth import authenticate_gmail

def list_labels():
    service = authenticate_gmail()
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])
    if not labels:
        print("Geen labels gevonden.")
    else:
        print("📌 Gmail-labels:")
        for label in labels:
            print(f"- {label['name']}")

if __name__ == "__main__":
    list_labels()