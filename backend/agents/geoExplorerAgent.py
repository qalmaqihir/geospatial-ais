import requests
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

# Define the response structure using Pydantic
class AgentResponse(BaseModel):
    text: str
    suggestions: List[Dict[str, str]]
    metadata: Dict[str, Any]

class GeoExplorerAgent:
    """Agent to fetch geographical information using various APIs."""
    
    def __init__(self):
        """Initialize the agent."""
        pass
    
    def get_location_info(self, location: str, coordinates: Optional[str] = None) -> dict:
        """
        Fetch geographical information about a location.
        
        Args:
            location (str): Name of the location (e.g., "Paris, France").
            coordinates (str, optional): Latitude and longitude as a string (e.g., "48.8566,2.3522").
        
        Returns:
            dict: Response containing text, suggestions, and metadata.
        """
        logger.info(f"Fetching location info for: {location}, Coordinates: {coordinates}. TOOL Calling for GEOExplorerAgent")
        try:
            from utils.geoUtils import reverse_geocode, geocode_location
            if coordinates is not None and coordinates.strip():
                # Attempt to parse coordinates from string format
                lat_lon = coordinates.split(',')
                if len(lat_lon) == 2:
                    try:
                        lat, lon = float(lat_lon[0]), float(lat_lon[1])
                        # Call reverse_geocode to get location details
                        rev_geo = reverse_geocode(lat, lon)
                        # If reverse_geocode returns a string, parse it
                        if isinstance(rev_geo, str):
                            parts = rev_geo.split(',')
                            if len(parts) >= 3:
                                country = parts[-1].strip()
                                region = parts[-2].strip()
                                city = parts[0].strip()
                            else:
                                country = "Unknown"
                                region = "Unknown"
                                city = rev_geo.strip()
                            location_info = {
                                "country": country,
                                "state": region,
                                "city": city,
                                "full_name": rev_geo
                            }
                        else:
                            # Assume reverse_geocode returned a dictionary
                            location_info = rev_geo
                    except ValueError:
                        # If coordinate parsing fails, fall back to geocode_location using location name
                        location_info = geocode_location(location)
                        lat, lon = location_info['lat'], location_info['lon']
                else:
                    # If coordinates format is invalid, fall back to geocode_location using location name
                    location_info = geocode_location(location)
                    lat, lon = location_info['lat'], location_info['lon']
            else:
                # Use location name if no coordinates provided
                location_info = geocode_location(location)
                lat, lon = location_info['lat'], location_info['lon']
                # Optionally try to enrich details via reverse_geocode
                try:
                    rev_geo = reverse_geocode(lat, lon)
                    if isinstance(rev_geo, str):
                        parts = rev_geo.split(',')
                        if len(parts) >= 3:
                            country = parts[-1].strip()
                            region = parts[-2].strip()
                            city = parts[0].strip()
                        else:
                            country = "Unknown"
                            region = "Unknown"
                            city = rev_geo.strip()
                        location_info = {
                            "country": country,
                            "state": region,
                            "city": city,
                            "full_name": rev_geo
                        }
                except Exception as e:
                    logger.warning(f"Reverse geocoding fallback failed: {e}")
            
            # Extract details from location_info dictionary
            country = location_info.get('country', 'Unknown')
            region = location_info.get('state', location_info.get('region', 'Unknown'))
            city = location_info.get('city', location_info.get('name', 'Unknown'))
            
            # Fetch additional country information (population, timezone, etc.) using REST Countries API
            try:
                if country != 'Unknown':
                    country_info_url = f"https://restcountries.com/v3.1/name/{country}?fields=name,population,capital,languages,currencies,timezones,flags"
                    country_response = requests.get(country_info_url)
                    if country_response.status_code == 200:
                        country_data = country_response.json()[0]
                        population = country_data.get('population', 'Unknown')
                        capital = country_data.get('capital', ['Unknown'])[0]
                        languages = ", ".join(country_data.get('languages', {}).values())
                        timezone = country_data.get('timezones', ['Unknown'])[0]
                    else:
                        population = capital = languages = timezone = "Unknown"
                else:
                    population = capital = languages = timezone = "Unknown"
            except Exception as e:
                logger.warning(f"Error fetching additional country info: {str(e)}")
                population = capital = languages = timezone = "Unknown"
            
            # Construct the response text and suggestions
            text = f"{city}, {region}, {country} is located at coordinates {lat}, {lon}. "
            if country != 'Unknown' and capital != 'Unknown':
                text += f"The country has a population of approximately {population:,} people. "
                text += f"The capital is {capital} and the main languages spoken are {languages}. "
                text += f"The primary timezone is {timezone}."
            
            suggestions = [
                {"label": "View on map", "action": f"map:{lat},{lon}"},
                {"label": "Get weather", "action": "get_weather"},
                {"label": "Find nearby places", "action": "find_nearby"}
            ]
            
            metadata = {
                "coordinates": f"{lat},{lon}",
                "location": {
                    "city": city,
                    "region": region,
                    "country": country,
                    "full_name": location_info.get('full_name', location)
                },
                "country_info": {
                    "population": population,
                    "capital": capital,
                    "languages": languages,
                    "timezone": timezone
                },
                "type": "location_info"
            }
            logger.info(f"Successfully fetched GeoExplorerAgent Data for: {location}\nText={text}\nSuugestions={suggestions}\nMetadata={metadata}")            
            return AgentResponse(text=text, suggestions=suggestions, metadata=metadata).model_dump()
        
        except Exception as e:
            logger.error(f"Error in get_location_info: {str(e)}")
            response = AgentResponse(
                text=f"Error fetching geographic information for {location}: {str(e)}",
                suggestions=[],
                metadata={"error": str(e), "location": location}
            )
            return response.model_dump()
