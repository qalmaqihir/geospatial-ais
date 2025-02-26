import requests
import os
from dotenv import load_dotenv

load_dotenv()

class ClimateImpactAgent:
    def __init__(self):
        self.noaa_api_key = os.getenv('NOAA_API_KEY')
        self.nasa_api_key = os.getenv('NASA_API_KEY')

    def analyze_climate_impact(self, coordinates):
        try:
            lat, lon = coordinates

            # NOAA Climate Data (simplified)
            noaa_url = f"https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&stationid=GHCND:USW00014734&startdate=2020-01-01&enddate=2025-01-01&limit=1000"
            noaa_response = requests.get(noaa_url, headers={'token': self.noaa_api_key})
            climate_data = noaa_response.json() if noaa_response.status_code == 200 else {}

            # NASA Climate Data
            nasa_url = f"https://power.larc.nasa.gov/api/temporal/climatology/point?parameters=T2M&community=RE&longitude={lon}&latitude={lat}&start=2020&end=2025&format=JSON"
            nasa_response = requests.get(nasa_url)
            nasa_data = nasa_response.json() if nasa_response.status_code == 200 else {}

            response = {
                "text": f"Climate impact analysis for {lat},{lon}:\nTemperature trends indicate {nasa_data.get('properties', {}).get('T2M', 'N/A')} over recent years, with NOAA data showing {climate_data.get('results', 'N/A')}.",
                "metadata": {
                    "coordinates": [lat, lon],
                    "type": "climate_impact"
                }
            }
            return response
        except Exception as e:
            print(f"ClimateImpactAgent error: {str(e)}")
            return {"text": f"Error fetching climate data: {str(e)}", "metadata": {"error": str(e)}}