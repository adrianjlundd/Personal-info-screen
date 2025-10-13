import requests

class BusFetcher:
    def __init__(self, stop_id, client_name="adrian-personalinfo-screen"):
        self.stop_id = stop_id
        self.url = "https://api.entur.io/journey-planner/v3/graphql"
        self.headers = {
            "Content-Type": "application/json",
            "ET-Client-Name": client_name
        }

    def list_next_buses(self, number_of_departures=6):
        query = f"""
        {{
          stopPlace(id: "{self.stop_id}") {{
            name
            estimatedCalls(timeRange: 7200, numberOfDepartures: 30) {{
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
            buses_to_sentrum = [
                call for call in stop["estimatedCalls"]
                if call["serviceJourney"]["line"]["transportMode"].lower() == "bus"
                and "sentrum" in call["destinationDisplay"]["frontText"].lower()
            ]
            results = []
            for call in buses_to_sentrum[:number_of_departures]:
                line = call["serviceJourney"]["line"]["publicCode"]
                dest = call["destinationDisplay"]["frontText"]
                time = call["expectedDepartureTime"]
                results.append(f"{time} → {dest} (linje {line})")
            return results
        except Exception as e:
            return [f"Error fetching buses: {e}"]
