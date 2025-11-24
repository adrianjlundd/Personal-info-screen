from __future__ import print_function
import datetime
import re
from zoneinfo import ZoneInfo  # krever Python 3.9+
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
LOCAL_TZ = ZoneInfo("Europe/Oslo")

class CalendarFetcher:
    def __init__(self, token_file):
        self.token_file = token_file
        self.creds = None
        self.service = None
        self._load_service()
    
    from google.auth.transport.requests import Request

    def _load_service(self):
        """Laster inn Google Calendar service fra token, med automatisk refresh."""
        try:
            self.creds = Credentials.from_authorized_user_file(self.token_file, SCOPES)
            
            # Refresh access token hvis den er utløpt
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
                # Lagre oppdatert token tilbake til filen
                with open(self.token_file, 'w') as token:
                    token.write(self.creds.to_json())
    
            self.service = build('calendar', 'v3', credentials=self.creds)
        except Exception as e:
            print(f"[CalendarFetcher] Feil ved lasting av {self.token_file}: {e}")

    
    def list_upcoming_events(self, days=2):
        """Returnerer hendelser i dag og neste <days> dager fra ALLE kalendere."""
        if not self.service:
            return ["(Feil: mangler Google Calendar-tilkobling)"]

        try:
            # Use timezone-aware UTC now
            now = datetime.datetime.now(datetime.timezone.utc)
            time_min = now.isoformat()
            time_max = (now + datetime.timedelta(days=days)).isoformat()

            all_events = []
            calendar_list = self.service.calendarList().list().execute().get('items', [])
            
            for cal in calendar_list:
                cal_id = cal['id']
                cal_name = cal.get('summary', 'Ukjent kalender')

                events_result = self.service.events().list(
                    calendarId=cal_id,
                    timeMin=time_min,
                    timeMax=time_max,
                    singleEvents=True,
                    orderBy='startTime'
                ).execute()
                events = events_result.get('items', [])
                
                for event in events:
                    start = event['start'].get('dateTime', event['start'].get('date'))
                    title = event.get('summary', '(uten tittel)')

                    # Fjern slike "NTNU TimeEdit"-kalendernavn
                    clean_cal_name = re.sub(r"\[TMA\d{4}[^]]*\]\s*", "", f"[{cal_name}] ")

                    all_events.append((start, f"{clean_cal_name}{title}"))

            if not all_events:
                return []

            # Sorter etter tidspunkt
            all_events.sort(key=lambda x: x[0])

            formatted_events = []
            for start, title in all_events:
                try:
                    if "T" in start:
                        dt = datetime.datetime.fromisoformat(start.replace("Z", "+00:00"))
                        dt_local = dt.astimezone(LOCAL_TZ)
                        tid = dt_local.strftime("%Y-%m-%d %H:%M")
                    else:
                        # start is a date-only string for all-day events (YYYY-MM-DD)
                        # Prefix with the ISO date so the caller can parse/group by date.
                        tid = f"{start} Hele dagen"
                    formatted_events.append(f"{tid} {title.strip()}")
                except Exception:
                    formatted_events.append(f"{start} {title.strip()}")
            
            # Fjern eventuelle tomme linjer eller doble mellomrom
            formatted_events = [re.sub(r"\s+", " ", e).strip() for e in formatted_events]

            return formatted_events

        except HttpError as e:
            print(f"[CalendarFetcher] HTTP-feil: {e}")
            return ["(Feil ved henting av kalender)"]
        except Exception as e:
            print(f"[CalendarFetcher] Uventet feil: {e}")
            return ["(Feil ved behandling av kalenderdata)"]
