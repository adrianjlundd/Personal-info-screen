import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Filene med tokens
TOKEN_FILES = ["token_abakus.json", "token_privat.json", "token_samf.json"]

# Google Calendar scope
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def load_events(token_file):
    """Laster events fra en bruker basert på token-fil"""
    creds = None
    with open(token_file, "r") as f:
        creds_data = json.load(f)
        creds = Credentials.from_authorized_user_info(creds_data, SCOPES)

    service = build('calendar', 'v3', credentials=creds)
    events_result = service.events().list(
        calendarId='primary',
        maxResults=5,  # hente f.eks. 5 neste events
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])
    return events

def main():
    for token_file in TOKEN_FILES:
        print(f"\n=== Events for {token_file} ===")
        try:
            events = load_events(token_file)
            if not events:
                print("Ingen kommende events.")
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(f"{start} - {event['summary']}")
        except Exception as e:
            print(f"Feil ved henting av events: {e}")

if __name__ == "__main__":
    main()
