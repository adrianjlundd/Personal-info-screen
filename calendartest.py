from __future__ import print_function
import datetime
import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

TOKEN_FILES = ["token_abakus.json", "token_privat.json", "token_samf.json"]
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# Sett inn epostene dine her når du vet hvem som er hvem
EMAILS = {
    "token_abakus.json": "adrianjlund@abakus.com",
    "token_privat.json": "adrianjlund@gmail.com",
    "token_samf.json": "adriajl@samf.com"
}

def test_calendar_access(token_file):
    try:
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
        service = build('calendar', 'v3', credentials=creds)

        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' = UTC time
        events_result = service.events().list(
            calendarId='primary', timeMin=now,
            maxResults=5, singleEvents=True,
            orderBy='startTime').execute()
        events = events_result.get('items', [])

        print(f"\n✅ Token '{token_file}' ({EMAILS.get(token_file, 'ukjent epost')}) fungerer.")
        if not events:
            print("Ingen kommende hendelser funnet.")
        else:
            print("Neste hendelser:")
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(f" - {start}: {event['summary']}")
    except FileNotFoundError:
        print(f"\n❌ Fant ikke token-fil: {token_file}")
    except HttpError as error:
        print(f"\n❌ Feil med token '{token_file}': {error}")
    except Exception as e:
        print(f"\n❌ Uventet feil for '{token_file}': {e}")

def main():
    print("Tester tilgang til Google Calendar:\n" + "="*40)
    for token_file in TOKEN_FILES:
        test_calendar_access(token_file)

if __name__ == '__main__':
    main()