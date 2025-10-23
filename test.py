from __future__ import print_function
import datetime
import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

TOKEN_FILES = ["token_abakus.json", "token_privat.json", "token_samf.json"]
EMAILS = {
    "token_abakus.json": "adrianjlund@abakus.com",
    "token_privat.json": "adrianjlund@gmail.com",
    "token_samf.json": "adriajl@samf.com"
}
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_time_window():
    """Return start (nå) og slutt (slutten av morgendagen) i RFC3339 format."""
    now = datetime.datetime.now(datetime.UTC)
    start = now.isoformat()
    end_of_tomorrow = (now + datetime.timedelta(days=2)).replace(
        hour=0, minute=0, second=0, microsecond=0
    ).isoformat()
    return start, end_of_tomorrow

def fetch_events_for_token(token_file):
    try:
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
        service = build('calendar', 'v3', credentials=creds)

        start, end = get_time_window()

        # Hent alle kalendere brukeren har tilgang til
        calendar_list = service.calendarList().list().execute().get('items', [])
        print(f"\n📅 Hendelser for {EMAILS.get(token_file)}:")
        print("=" * 60)

        all_events = []
        for cal in calendar_list:
            cal_id = cal['id']
            cal_summary = cal.get('summary', 'Ukjent kalender')

            events_result = service.events().list(
                calendarId=cal_id,
                timeMin=start,
                timeMax=end,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            events = events_result.get('items', [])

            if not events:
                continue

            for event in events:
                start_time = event['start'].get('dateTime', event['start'].get('date'))
                all_events.append((start_time, cal_summary, event.get('summary', '(uten tittel)')))

        if not all_events:
            print("Ingen hendelser i dag eller i morgen.")
        else:
            # Sorter alle hendelser etter tid
            all_events.sort(key=lambda x: x[0])
            for start_time, cal_name, title in all_events:
                print(f"{start_time} | [{cal_name}] {title}")

    except HttpError as error:
        print(f"❌ Feil med token '{token_file}': {error}")
    except Exception as e:
        print(f"❌ Uventet feil for '{token_file}': {e}")

def main():
    print("=== Henter hendelser i dag og i morgen fra alle kalendere ===")
    for token_file in TOKEN_FILES:
        fetch_events_for_token(token_file)

if __name__ == '__main__':
    main()
