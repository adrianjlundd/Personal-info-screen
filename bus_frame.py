import requests
from datetime import datetime
import json
from zoneinfo import ZoneInfo

class BusFetcher:
    def __init__(self, stop_id, client_name="adrian-personalinfo-screen"):
        self.stop_id = stop_id
        self.url = "https://api.entur.io/journey-planner/v3/graphql"
        self.headers = {
            "Content-Type": "application/json",
            "ET-Client-Name": client_name
        }

    def list_next_buses(self, number_of_departures=6):
        query = """
        {
          stopPlace(id: "%s") {
            name
            estimatedCalls(timeRange: 7200, numberOfDepartures: 20) {
              realtime
              expectedDepartureTime
              destinationDisplay {
                frontText
              }
              serviceJourney {
                line {
                  publicCode
                  transportMode
                }
              }
            }
          }
        }
        """ % self.stop_id
        
        try:
            response = requests.post(self.url, headers=self.headers, json={"query": query})
            response.raise_for_status()
            data = response.json()
            
            # Debug: print raw data
            #print("Raw bus data:", json.dumps(data, indent=2)[:500] + "...")
            
            stop = data["data"]["stopPlace"]
            if not stop or "estimatedCalls" not in stop:
                return ["Ingen bussdata tilgjengelig"]
            
            # Filter buses to Sentrum and sort by time
            buses_to_sentrum = [
                call for call in stop["estimatedCalls"]
                if call["serviceJourney"]["line"]["transportMode"].lower() == "bus"
                and "sentrum" in call["destinationDisplay"]["frontText"].lower()
            ]
            
            # Sort by departure time
            buses_to_sentrum.sort(key=lambda x: x["expectedDepartureTime"])
            
            results = []
            for call in buses_to_sentrum[:number_of_departures]:
                line = call["serviceJourney"]["line"]["publicCode"]
                dest = call["destinationDisplay"]["frontText"]
                departure_time = call["expectedDepartureTime"]
                
                # Calculate minutes until departure
                dep_dt = datetime.fromisoformat(departure_time.replace('Z', '+00:00')).astimezone(ZoneInfo("Europe/Oslo"))
                now = datetime.now(ZoneInfo("Europe/Oslo"))
                minutes_until = int((dep_dt - now).total_seconds() / 60)

                
                # Only show buses departing in the future or very recently
                if minutes_until >= -1:  # Allow 1 minute tolerance for "now"
                    if minutes_until <= 0:
                        results.append(f"Linje {line} → {dest} - NÅ")
                    elif minutes_until == 1:
                        results.append(f"Linje {line} → {dest} - 1 min")
                    else:
                        results.append(f"Linje {line} → {dest} - {minutes_until} min")
            
            return results if results else ["Ingen avganger til Sentrum"]
            
        except Exception as e:
            print(f"Bus API error: {e}")
            return [f"Feil: {e}"]