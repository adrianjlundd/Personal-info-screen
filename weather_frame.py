import requests
import os
from dotenv import load_dotenv

load_dotenv()

class WeatherFetcher:
    def __init__(self, city="Trondheim,no"):
        self.api_key = os.getenv("OPENWEATHERMAP_KEY")
        self.city = city

    def get_weather(self):
        if not self.api_key:
            return "API-nøkkel for vær er ikke satt"
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={self.api_key}&units=metric&lang=no"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            temp = round(data['main']['temp'])
            feels_like = round(data['main']['feels_like'])
            desc = data['weather'][0]['description'].capitalize()
            humidity = data['main']['humidity']
            
            weather_emoji = self.get_weather_emoji(data['weather'][0]['main'])
            
            return f"{weather_emoji} {temp}°C (føles som {feels_like}°C) • {desc} • Fuktighet: {humidity}%"
            
        except Exception as e:
            return f"Feil ved henting av vær: {e}"
    
    def get_weather_emoji(self, weather_main):
        emoji_map = {
            'Clear': '☀️',
            'Clouds': '☁️',
            'Rain': '🌧️',
            'Drizzle': '🌦️',
            'Thunderstorm': '⛈️',
            'Snow': '❄️',
            'Mist': '🌫️',
            'Fog': '🌫️'
        }
        return emoji_map.get(weather_main, '🌤️')