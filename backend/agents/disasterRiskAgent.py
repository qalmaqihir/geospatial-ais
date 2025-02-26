import requests
import os
from dotenv import load_dotenv

load_dotenv()

class DisasterRiskAgent:
    def __init__(self):
        self.usgs_api = os.getenv('USGS_API_KEY')

    def assess_disaster_risk(self, coordinates):
        try:
            lat, lon = coordinates

            # USGS Earthquake Data
            usgs_url = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&latitude={lat}&longitude={lon}&maxradius=5&minmagnitude=2"
            usgs_response = requests.get(usgs_url)
            earthquakes = usgs_response.json()['features'] if usgs_response.status_code == 200 else []

            # Weather Alerts (simplified, using NOAA or similar)
            weather_url = f"https://api.weather.gov/points/{lat},{lon}"
            weather_response = requests.get(weather_url)
            weather_data = weather_response.json() if weather_response.status_code == 200 else {}

            response = {
                "text": f"Disaster risk near {lat},{lon}:\n{len(earthquakes)} recent earthquakes detected, weather alerts show {weather_data.get('properties', {}).get('forecast', 'N/A')}.",
                "metadata": {
                    "coordinates": [lat, lon],
                    "type": "disaster_risk"
                }
            }
            return response
        except Exception as e:
            print(f"DisasterRiskAgent error: {str(e)}")
            return {"text": f"Error assessing disaster risk: {str(e)}", "metadata": {"error": str(e)}}