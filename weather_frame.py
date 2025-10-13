import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Leser .env

class WeatherFetcher:
    def __init__(self, city="Trondheim,no"):
        self.api_key = os.getenv("OPENWEATHERMAP_KEY")
        self.city = city

    def get_weather(self):
        if not self.api_key:
            return "API key not set"
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={self.api_key}&units=metric"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            temp = data['main']['temp']
            desc = data['weather'][0]['description']
            return f"{self.city.split(',')[0]}: {temp}°C, {desc}"
        except Exception as e:
            return f"Error fetching weather: {e}"
