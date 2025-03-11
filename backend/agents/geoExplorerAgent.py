import wikipedia
from utils.geoUtils import geocode_location, reverse_geocode
import logging
from pydantic import BaseModel
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

# Define the response structure using Pydantic
class AgentResponse(BaseModel):
    text: str
    suggestions: List[Dict[str, str]]
    metadata: Dict[str, Any]

class GeoExplorerAgent:
    """Agent to fetch geographical information from Wikipedia."""
    
    def __init__(self):
        """Initialize the agent with an empty cache."""
        self.cache = {}
    
    def get_location_info(self, location: str = None, coordinates: tuple[float, float] = None) -> dict:
        """
        Fetch location information using either a location name or coordinates.
        
        Args:
            location (str, optional): Name of the location (e.g., "Paris").
            coordinates (tuple[float, float], optional): Latitude and longitude (e.g., (48.8566, 2.3522)).
        
        Returns:
            dict: Response containing text, suggestions, and metadata.
                  - text: Summary or error message.
                  - suggestions: List of actionable links (e.g., Wikipedia URL).
                  - metadata: Additional info like coordinates or error details.
        
        Raises:
            ValueError: If neither location nor coordinates are provided.
        """
        try:
            # Determine location name and coordinates
            if location is not None:
                result = geocode_location(location)
                lat, lon = result['lat'], result['lon']
                location_name = location
            elif coordinates is not None:
                lat, lon = coordinates
                location_name = reverse_geocode(lat, lon)
            else:
                raise ValueError("Either location or coordinates must be provided")
            
            # Check cache first
            if location_name in self.cache:
                return self.cache[location_name]
            
            # Fetch Wikipedia data
            try:
                page = wikipedia.page(location_name, auto_suggest=False)
                summary = page.summary
                url = page.url
                response = AgentResponse(
                    text=summary,
                    suggestions=[{"label": f"Read more about {location_name}", "action": url}],
                    metadata={"coordinates": [lat, lon], "type": "geographical_info"}
                )
                self.cache[location_name] = response.model_dump()
                return response.model_dump()
            except wikipedia.PageError:
                response = AgentResponse(
                    text=f"No Wikipedia page found for {location_name}",
                    suggestions=[],
                    metadata={"coordinates": [lat, lon], "type": "geographical_info"}
                )
                return response.model_dump()
            except Exception as e:
                logger.error(f"Error fetching Wikipedia data: {str(e)}")
                response = AgentResponse(
                    text=f"Error fetching data: {str(e)}",
                    suggestions=[],
                    metadata={"error": str(e)}
                )
                return response.model_dump()
        except Exception as e:
            logger.error(f"Error in get_location_info: {str(e)}")
            response = AgentResponse(
                text=f"Error: {str(e)}",
                suggestions=[],
                metadata={"error": str(e)}
            )
            return response.model_dump()