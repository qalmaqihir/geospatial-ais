import wikipedia
from utils.geoUtils import geocode_location
import logging

logger = logging.getLogger(__name__)

class GeoExplorerAgent:
    def __init__(self):
        self.cache = {}

    def get_location_info(self, location, coordinates=None):
        try:
            if coordinates:
                lat, lon = coordinates
            else:
                result = geocode_location(location)
                lat, lon = result['lat'], result['lon']

            # Fetch from Wikipedia/Wikidata
            location_name = location if isinstance(location, str) else f"{lat},{lon}"
            if location_name in self.cache:
                return self.cache[location_name]

            # Search Wikipedia for location details
            wiki_summary = wikipedia.summary(location_name, sentences=3)
            wiki_url = wikipedia.page(location_name).url

            response = {
                "text": f"Location details for {location_name}:\n{wiki_summary}",
                "metadata": {
                    "coordinates": [lat, lon],
                    "url": wiki_url,
                    "type": "geographical_info"
                }
            }
            self.cache[location_name] = response
            return response
        except Exception as e:
            logger.error(f"GeoExplorerAgent error: {str(e)}")
            return {"text": f"Error fetching location info: {str(e)}", "metadata": {"error": str(e)}}