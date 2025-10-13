import requests
import json

# GraphQL-endepunkt
url = "https://api.entur.io/journey-planner/v3/graphql"

# Header som identifiserer deg
headers = {
    "Content-Type": "application/json",
    "ET-Client-Name": "adrianjlundd-personlig-info-skjerm"
}

# GraphQL-spørring: henter mange avganger (30) for å ha nok å filtrere
query = """
{
  stopPlace(id: "NSR:StopPlace:43133") {
    name
    estimatedCalls(timeRange: 7200, numberOfDepartures: 30) {
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
"""

# Send forespørselen
response = requests.post(url, headers=headers, json={"query": query})

# Sjekk status
if response.status_code != 200:
    print(f"Feil ({response.status_code}):", response.text)
else:
    data = response.json()
    stop = data["data"]["stopPlace"]
    print(f"🚌 Avganger fra: {stop['name']}\n")

    # Filtrer avganger: bare buss mot sentrum
    buses_to_sentrum = [
        call for call in stop["estimatedCalls"]
        if call["serviceJourney"]["line"]["transportMode"].lower() == "bus"
        and "sentrum" in call["destinationDisplay"]["frontText"].lower()
    ]

    if not buses_to_sentrum:
        print("Ingen bussavganger mot sentrum i løpet av de neste 2 timene.")
    else:
        # Vis de 6 neste
        for call in buses_to_sentrum[:6]:
            line = call["serviceJourney"]["line"]["publicCode"]
            dest = call["destinationDisplay"]["frontText"]
            time = call["expectedDepartureTime"]
            print(f"{time} → {dest} (linje {line})")