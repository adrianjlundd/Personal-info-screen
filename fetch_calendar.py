# calendar_fetch.py
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TOKEN_FILES = ["token_abakus.json", "token_privat.json", "token_samf.json"]
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def list_upcoming_events():
    all_events = []
    for token_file in TOKEN_FILES:
        try:
            with open(token_file, "r") as f:
                creds_data = json.load(f)
                creds = Credentials.from_authorized_user_info(creds_data, SCOPES)

            service = build('calendar', 'v3', credentials=creds)
            events_result = service.events().list(
                calendarId='primary',
                maxResults=5,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            events = events_result.get('items', [])
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                all_events.append({"user": token_file, "start": start, "summary": event.get("summary", "")})
        except Exception as e:
            all_events.append({"user": token_file, "error": str(e)})
    return all_events
