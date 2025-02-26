import requests
import os
from dotenv import load_dotenv

load_dotenv()

class EcoFootprintAgent:
    def __init__(self):
        self.noaa_api = os.getenv('NOAA_API_KEY')

    def analyze_eco_footprint(self, coordinates):
        try:
            lat, lon = coordinates

            # NOAA Pollution Data
            pollution_url = f"https://www.airnowapi.org/aq/observation/latLong/current/?format=application/json&latitude={lat}&longitude={lon}&distance=25&API_KEY={self.noaa_api}"
            pollution_response = requests.get(pollution_url)
            pollution_data = pollution_response.json() if pollution_response.status_code == 200 else {}

            # Satellite Imagery for Deforestation (simplified)
            sat_url = f"https://api.nasa.gov/planetary/earth/assets?lon={lon}&lat={lat}&date=2023-01-01&dim=0.10&api_key={os.getenv('NASA_API_KEY')}"
            sat_response = requests.get(sat_url)
            deforestation = sat_response.json() if sat_response.status_code == 200 else {}

            response = {
                "text": f"Eco footprint near {lat},{lon}:\nPollution level: {pollution_data.get('data', 'N/A')}, deforestation risk: {deforestation.get('status', 'N/A')}.",
                "metadata": {
                    "coordinates": [lat, lon],
                    "type": "eco_footprint"
                }
            }
            return response
        except Exception as e:
            print(f"EcoFootprintAgent error: {str(e)}")
            return {"text": f"Error analyzing eco footprint: {str(e)}", "metadata": {"error": str(e)}}