import requests
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class AgentResponse(BaseModel):
    text: str
    suggestions: List[Dict[str, str]]
    metadata: Dict[str, Any]

class InfoAgent:
    """Agent to fetch regional information (history, culture, and cuisine) from Wikipedia."""
    
    def __init__(self):
        """Initialize the agent."""
        pass
    
    def get_info(self, location: str, coordinates: Optional[str] = None) -> dict:
        """
        Fetch regional information about history, culture, and cuisine from Wikipedia.
        
        Args:
            location (str): The name of the region (e.g., "Rawalpindi").
            coordinates (Optional[str]): Coordinates in "lat,lon" format (optional).
        
        Returns:
            dict: A response containing a summary text, suggestions, and metadata.
        """
        logger.info(f"Fetching location info for: {location}, Coordinates: {coordinates}. TOOL Calling for INFOAgent")

        try:
            # If location is empty and coordinates are provided, try to resolve the name.
            if not location or not location.strip():
                from utils.geoUtils import reverse_geocode
                if coordinates:
                    lat_str, lon_str = coordinates.split(',')
                    lat, lon = float(lat_str.strip()), float(lon_str.strip())
                    location = reverse_geocode(lat, lon)
                else:
                    raise ValueError("Location information is required.")
            
            # Create queries for different aspects.
            queries = {
                "History": f"History of {location}",
                "Culture": f"Culture of {location}",
                "Cuisine": f"Cuisine of {location}"
            }
            
            info_parts = {}
            for key, query in queries.items():
                params = {
                    "action": "query",
                    "format": "json",
                    "prop": "extracts",
                    "exintro": True,
                    "explaintext": True,
                    "titles": query
                }
                response = requests.get("https://en.wikipedia.org/w/api.php", params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
                pages = data.get("query", {}).get("pages", {})
                extract = None
                for page_id in pages:
                    page = pages[page_id]
                    if "extract" in page and page["extract"]:
                        extract = page["extract"]
                        break
                if extract:
                    info_parts[key] = extract.strip()
                else:
                    info_parts[key] = f"No information on {key.lower()} available for {location}."
            
            text = (f"Regional Information for {location}:\n\n"
                    f"History: {info_parts['History']}\n\n"
                    f"Culture: {info_parts['Culture']}\n\n"
                    f"Cuisine: {info_parts['Cuisine']}")
            
            suggestions = [
                {"label": "View Wikipedia", "action": f"https://en.wikipedia.org/wiki/{location.replace(' ', '_')}"}
            ]
            
            metadata = {
                "location": location,
                "info": info_parts,
                "type": "regional_info"
            }
            logger.info(f"Successfully fetched infoAgent Data for: {location}\nText={text}\nSuugestions={suggestions}\nMetadata={metadata}")
            return AgentResponse(text=text, suggestions=suggestions, metadata=metadata).model_dump()
        
        except Exception as e:
            logger.error(f"Error in get_info: {str(e)}")
            response = AgentResponse(
                text=f"Error fetching regional information for {location}: {str(e)}",
                suggestions=[],
                metadata={"error": str(e), "location": location}
            )
            return response.model_dump()
