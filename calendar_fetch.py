import json
from datetime import datetime, timezone
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TOKEN_FILES = ["token_abakus.json", "token_privat.json", "token_samf.json"]
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

class CalendarFetcher:
    def list_upcoming_events(self):
        all_events = []
        now = datetime.now(timezone.utc)
        for token_file in TOKEN_FILES:
            try:
                with open(token_file, "r") as f:
                    creds_data = json.load(f)
                    creds = Credentials.from_authorized_user_info(creds_data, SCOPES)

                service = build('calendar', 'v3', credentials=creds)
                events_result = service.events().list(
                    calendarId='primary',
                    maxResults=10,
                    singleEvents=True,
                    orderBy='startTime',
                    timeMin=now.isoformat()
                ).execute()
                events = events_result.get('items', [])
                for event in events:
                    start = event['start'].get('dateTime', event['start'].get('date'))
                    summary = event.get('summary', '')
                    all_events.append(f"{start} → {summary} ({token_file})")
            except Exception as e:
                all_events.append(f"Feil med {token_file}: {e}")
        return all_events
