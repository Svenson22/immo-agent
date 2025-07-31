from gmail_auth import authenticate_gmail
import base64

def fetch_emails(query="newer_than:7d", max_results=50):
    """
    Haalt e-mails op uit Gmail op basis van een query (standaard: mails van afgelopen 7 dagen).
    query: Gmail zoekopdracht (bv. newer_than:7d)
    max_results: maximaal aantal mails om op te halen
    """
    service = authenticate_gmail()

    # ✅ Zoek e-mails met query
    results = service.users().messages().list(
        userId='me', q=query, maxResults=max_results
    ).execute()

    messages = results.get('messages', [])
    print(f"📌 {len(messages)} berichten gevonden met query '{query}'")
    if not messages:
        print("Geen mails gevonden.")
        return []

    emails = []

    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()

        # ✅ Haal onderwerp op
        headers = msg_data.get('payload', {}).get('headers', [])
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), "Geen onderwerp")

        # ✅ Labels voor debug
        labels = msg_data.get('labelIds', [])
        print(f"➡ Verwerk mail: '{subject}' | Labels: {labels}")

        # ✅ Body decoderen (inclusief nested parts)
        def extract_body(parts):
            text = ''
            for part in parts:
                if part['mimeType'] in ['text/plain', 'text/html']:
                    if 'data' in part['body']:
                        text += base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                elif part.get('parts'):
                    text += extract_body(part['parts'])
            return text

        payload = msg_data.get('payload', {})
        body = ''
        if 'parts' in payload:
            body = extract_body(payload['parts'])
        else:
            if 'body' in payload and 'data' in payload['body']:
                body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')

        emails.append({"id": msg['id'], "subject": subject, "body": body})

    return emails

if __name__ == "__main__":
    mails = fetch_emails()
    print(f"\n✅ {len(mails)} e-mails opgehaald")
    for i, mail in enumerate(mails, start=1):
        print(f"\n📧 E-mail {i}: {mail['subject']}")
        print(mail['body'][:500])  # Toon eerste 500 tekens