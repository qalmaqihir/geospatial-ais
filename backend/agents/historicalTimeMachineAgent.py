import requests
import os
from dotenv import load_dotenv

load_dotenv()

class HistoricalTimeMachineAgent:
    def __init__(self):
        self.loc_api = os.getenv('LIBRARY_OF_CONGRESS_API_KEY')

    def get_historical_data(self, coordinates):
        try:
            lat, lon = coordinates

            # Library of Congress Historical Maps
            loc_url = f"https://www.loc.gov/maps/?q={lat},{lon}&fo=json"
            loc_response = requests.get(loc_url)
            historical_maps = loc_response.json()['results'] if loc_response.status_code == 200 else []

            response = {
                "text": f"Historical insights for {lat},{lon}:\nFound {len(historical_maps)} historical maps or photos.",
                "metadata": {
                    "coordinates": [lat, lon],
                    "urls": [map['url'] for map in historical_maps[:3]],
                    "type": "historical_data"
                }
            }
            return response
        except Exception as e:
            print(f"HistoricalTimeMachineAgent error: {str(e)}")
            return {"text": f"Error fetching historical data: {str(e)}", "metadata": {"error": str(e)}}