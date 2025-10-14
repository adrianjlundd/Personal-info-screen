from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import os
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

class CalendarFetcher:
    def __init__(self, token_file):
        self.SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
        self.token_file = token_file
        self.service = self.authenticate()
    
    def authenticate(self):
        creds = None
        
        if os.path.exists(self.token_file):
            try:
                with open(self.token_file, 'r') as token:
                    token_data = json.load(token)
                
                creds = Credentials(
                    token=token_data.get('token'),
                    refresh_token=token_data.get('refresh_token'),
                    token_uri=token_data.get('token_uri'),
                    client_id=token_data.get('client_id'),
                    client_secret=token_data.get('client_secret'),
                    scopes=self.SCOPES
                )
                
                print(f"Loaded token from {self.token_file}")
                
            except Exception as e:
                print(f"Error loading credentials from {self.token_file}: {e}")
                creds = None
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    print(f"Refreshed token for {self.token_file}")
                except Exception as e:
                    print(f"Error refreshing token for {self.token_file}: {e}")
                    creds = None
            else:
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json', self.SCOPES)
                    creds = flow.run_local_server(port=0)
                    print(f"Created new token for {self.token_file}")
                except Exception as e:
                    print(f"Error creating new token for {self.token_file}: {e}")
                    return None
            
            if creds:
                try:
                    token_data = {
                        'token': creds.token,
                        'refresh_token': creds.refresh_token,
                        'token_uri': creds.token_uri,
                        'client_id': creds.client_id,
                        'client_secret': creds.client_secret,
                        'scopes': creds.scopes
                    }
                    with open(self.token_file, 'w') as token:
                        json.dump(token_data, token)
                    print(f"Saved token to {self.token_file}")
                except Exception as e:
                    print(f"Error saving token to {self.token_file}: {e}")
        
        if creds:
            return build('calendar', 'v3', credentials=creds)
        else:
            print(f"Failed to authenticate for {self.token_file}")
            return None
    
    def list_upcoming_events(self, days=2, max_results=10):
        """Henter events for de neste 'days' dagene"""
        if not self.service:
            return ["Kalender ikke tilgjengelig"]
            
        try:
            oslo = ZoneInfo("Europe/Oslo")
            now = datetime.now(oslo).isoformat()
            end_time = (datetime.now(oslo) + timedelta(days=days)).isoformat()

            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=now,
                timeMax=end_time,
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            formatted_events = []
            today = datetime.now(oslo).date()
            tomorrow = (datetime.now(oslo) + timedelta(days=1)).date()
            
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                summary = event.get('summary', 'Ingen tittel')
                
                if 'T' in start:
                    event_dt = datetime.fromisoformat(start.replace('Z', '+00:00')).astimezone(oslo)

                    if event_dt.date() == today:
                        time_str = event_dt.strftime("%H:%M")
                        formatted_events.append(f"I dag {time_str} - {summary}")
                    elif event_dt.date() == tomorrow:
                        time_str = event_dt.strftime("%H:%M")
                        formatted_events.append(f"I morgen {time_str} - {summary}")
                    else:
                        date_str = event_dt.strftime("%d.%m kl. %H:%M")
                        formatted_events.append(f"{date_str} - {summary}")
                else:
                    event_date = datetime.fromisoformat(start)
                    if event_date.date() == today:
                        formatted_events.append(f"I dag - {summary} (hele dagen)")
                    elif event_date.date() == tomorrow:
                        formatted_events.append(f"I morgen - {summary} (hele dagen)")
                    else:
                        date_str = event_date.strftime("%d.%m")
                        formatted_events.append(f"{date_str} - {summary} (hele dagen)")
            
            return formatted_events
            
        except Exception as e:
            print(f"Calendar API error for {self.token_file}: {e}")
            return [f"Feil ved henting av kalender"]
