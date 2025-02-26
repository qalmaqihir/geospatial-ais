import requests
import os
from dotenv import load_dotenv

load_dotenv()

class DeepSeaAgent:
    def __init__(self):
        self.gebco_api = os.getenv('GEBCO_API_KEY')
        self.noaa_api = os.getenv('NOAA_API_KEY')

    def analyze_deep_sea(self, coordinates):
        try:
            lat, lon = coordinates

            # GEBCO Bathymetry Data
            gebco_url = f"https://www.gebco.net/api/v1/bathymetry?lat={lat}&lon={lon}"
            gebco_response = requests.get(gebco_url)
            depth = gebco_response.json()['elevation'] if gebco_response.status_code == 200 else None

            # NOAA Marine Data
            noaa_url = f"https://www.ncei.noaa.gov/thredds/ncss/grid/gebco2023/GEBCO_2023.nc?var=elevation&latitude={lat}&longitude={lon}"
            noaa_response = requests.get(noaa_url)
            marine_data = noaa_response.json() if noaa_response.status_code == 200 else {}

            response = {
                "text": f"Deep sea insights near {lat},{lon}:\nOcean depth is {depth} meters, with marine data showing {marine_data.get('properties', {}).get('elevation', 'N/A')}.",
                "metadata": {
                    "coordinates": [lat, lon],
                    "type": "deep_sea"
                }
            }
            return response
        except Exception as e:
            print(f"DeepSeaAgent error: {str(e)}")
            return {"text": f"Error analyzing deep sea: {str(e)}", "metadata": {"error": str(e)}}