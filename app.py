from flask import Flask, jsonify
from fetch_calendar import list_upcoming_events  # <-- nytt navn

app = Flask(__name__)

@app.route("/events")
def events():
    events = list_upcoming_events()
    return jsonify(events)

if __name__ == "__main__":
    app.run(debug=True)
