import requests
from datetime import datetime

class BusFetcher:
    def __init__(self, stop_id, client_name="adrian-personalinfo-screen"):
        self.stop_id = stop_id
        self.url = "https://api.entur.io/journey-planner/v3/graphql"
        self.headers = {
            "Content-Type": "application/json",
            "ET-Client-Name": client_name
        }

    def list_next_buses(self, number_of_departures=4):
        query = f"""
        {{
          stopPlace(id: "{self.stop_id}") {{
            name
            estimatedCalls(timeRange: 7200, numberOfDepartures: 20) {{
              expectedDepartureTime
              destinationDisplay {{
                frontText
              }}
              serviceJourney {{
                line {{
                  publicCode
                  transportMode
                }}
              }}
            }}
          }}
        }}
        """
        try:
            response = requests.post(self.url, headers=self.headers, json={"query": query})
            response.raise_for_status()
            data = response.json()
            stop = data["data"]["stopPlace"]
            
            # Filter buses to Sentrum
            buses_to_sentrum = [
                call for call in stop["estimatedCalls"]
                if call["serviceJourney"]["line"]["transportMode"].lower() == "bus"
                and "sentrum" in call["destinationDisplay"]["frontText"].lower()
            ]
            
            results = []
            for call in buses_to_sentrum[:number_of_departures]:
                line = call["serviceJourney"]["line"]["publicCode"]
                dest = call["destinationDisplay"]["frontText"]
                departure_time = call["expectedDepartureTime"]
                
                # Calculate minutes until departure
                dep_dt = datetime.fromisoformat(departure_time.replace('Z', '+00:00'))
                now = datetime.utcnow().replace(tzinfo=dep_dt.tzinfo)
                minutes_until = int((dep_dt - now).total_seconds() / 60)
                
                if minutes_until <= 0:
                    results.append(f"Linje {line} → {dest} - NÅ")
                elif minutes_until == 1:
                    results.append(f"Linje {line} → {dest} - om 1 minutt")
                else:
                    results.append(f"Linje {line} → {dest} - om {minutes_until} minutter")
            
            return results if results else ["Ingen avganger til Sentrum de neste timene"]
            
        except Exception as e:
            return [f"Feil ved henting av busser: {e}"]