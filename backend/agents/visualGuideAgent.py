from googlemaps import Client
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class VisualGuideAgent:
    def __init__(self):
        self.gmaps = Client(key=os.getenv('GOOGLE_MAPS_API_KEY'))
        self.nasa_api_key = os.getenv('NASA_API_KEY')

    def get_visual_data(self, coordinates):
        try:
            lat, lon = coordinates

            # Google Maps Static Image
            static_map_url = self.gmaps.static_map(
                center=f"{lat},{lon}",
                zoom=13,
                size=(600, 400),
                format="png",
                maptype="satellite"
            )

            # NASA Earth Observations (simplified)
            neo_url = f"https://api.nasa.gov/planetary/earth/imagery?lon={lon}&lat={lat}&api_key={self.nasa_api_key}"
            neo_response = requests.get(neo_url)
            neo_image = neo_response.url if neo_response.status_code == 200 else None

            response = {
                "text": "Here are visual insights for your location:",
                "metadata": {
                    "google_map_url": static_map_url,
                    "nasa_image_url": neo_image,
                    "type": "visual_data"
                }
            }
            return response
        except Exception as e:
            print(f"VisualGuideAgent error: {str(e)}")
            return {"text": f"Error fetching visual data: {str(e)}", "metadata": {"error": str(e)}}