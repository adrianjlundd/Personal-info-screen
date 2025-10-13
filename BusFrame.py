import requests
from datetime import datetime, timezone

class BusFetcher:
    def __init__(self, stop_id):
        self.stop_id = stop_id
        self.url = "https://api.entur.io/journey-planner/v3/graphql"
        self.headers = {"Content-Type": "application/json",
                        "ET-Client-Name": "adrian-personalinfo-screen"}
        self.query_template = """
        {{
          stopPlace(id: "{stop_id}") {{
            name
            estimatedCalls(timeRange: 7200, numberOfDepartures: 6) {{
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

    def list_next_buses(self):
        query = self.query_template.format(stop_id=self.stop_id)
        try:
            response = requests.post(self.url, headers=self.headers, json={"query": query})
            response.raise_for_status()
            data = response.json()
            stop = data["data"]["stopPlace"]
            bus_list = []
            now = datetime.now(timezone.utc)
            for call in stop["estimatedCalls"]:
                line = call["serviceJourney"]["line"]["publicCode"]
                dest = call["destinationDisplay"]["frontText"]
                dep_time = datetime.fromisoformat(call["expectedDepartureTime"])
                minutes = int((dep_time - now).total_seconds() / 60)
                bus_list.append(f"{line} → {dest} om {minutes} min")
            return bus_list
        except Exception as e:
            return [f"Feil med buss: {e}"]
