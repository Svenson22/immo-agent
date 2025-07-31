from __future__ import print_function
import os.path
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# 📌 SCOPES = machtigingen voor Gmail
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    creds = None
    
    # ✅ Check of token al bestaat (dus we hebben al ingelogd)
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # ✅ Als token niet bestaat, start de OAuth flow
    if not creds:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)  # Opent browser voor login
        
        # ✅ Bewaar token voor volgende keer (zodat je niet opnieuw moet inloggen)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    # ✅ Bouw een Gmail service object om API-aanroepen te doen
    return build('gmail', 'v1', credentials=creds)

if __name__ == "__main__":
    service = authenticate_gmail()
    print("✅ Gmail API verbonden!")