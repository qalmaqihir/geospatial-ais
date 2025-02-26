from googlemaps import Client
import os
from dotenv import load_dotenv

load_dotenv()

class TravelPlannerAgent:
    def __init__(self):
        self.gmaps = Client(key=os.getenv('GOOGLE_MAPS_API_KEY'))

    def plan_travel(self, coordinates, query="nearby attractions"):
        try:
            lat, lon = coordinates

            # Fetch nearby places
            places_result = self.gmaps.places_nearby(
                location=f"{lat},{lon}",
                radius=5000,
                keyword=query
            )

            suggestions = [
                {
                    "label": place['name'],
                    "action": place.get('website', f"https://www.google.com/maps/place/?q={place['name']}")
                } for place in places_result['results'][:3]
            ]

            response = {
                "text": f"Travel suggestions near {lat},{lon}:\n{suggestions[0]['label']} and more.",
                "suggestions": suggestions,
                "metadata": {
                    "coordinates": [lat, lon],
                    "type": "travel_plan"
                }
            }
            return response
        except Exception as e:
            print(f"TravelPlannerAgent error: {str(e)}")
            return {"text": f"Error planning travel: {str(e)}", "metadata": {"error": str(e)}}