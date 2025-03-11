import requests
from pydantic import BaseModel
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

# Define the response structure using Pydantic
class AgentResponse(BaseModel):
    text: str
    suggestions: List[Dict[str, str]]
    metadata: Dict[str, Any]

class ClimateImpactAgent:
    """Agent to fetch climate and weather information using Open-Meteo API."""
    
    def __init__(self):
        """Initialize the agent."""
        pass
    
    def get_weather_info(self, location: str = None, coordinates: tuple[float, float] = None) -> dict:
        """
        Fetch weather information using either a location name or coordinates.
        
        Args:
            location (str, optional): Name of the location (e.g., "Paris").
            coordinates (tuple[float, float], optional): Latitude and longitude (e.g., (48.8566, 2.3522)).
        
        Returns:
            dict: Response containing text, suggestions, and metadata.
                  - text: Weather summary or error message.
                  - suggestions: List of actionable links (e.g., weather forecast URL).
                  - metadata: Additional info like coordinates or error details.
        
        Raises:
            ValueError: If neither location nor coordinates are provided.
        """
        try:
            # Determine coordinates
            if coordinates is not None:
                lat, lon = coordinates
            elif location is not None:
                from utils.geoUtils import geocode_location
                result = geocode_location(location)
                lat, lon = result['lat'], result['lon']
            else:
                raise ValueError("Either location or coordinates must be provided")
            
            # Fetch weather data from Open-Meteo API
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            # Extract current weather
            current = data['current_weather']
            temperature = current['temperature']
            windspeed = current['windspeed']
            weather_code = current['weathercode']
            
            # Simple weather description based on code
            weather_desc = {
                0: "Clear sky",
                1: "Mainly clear",
                2: "Partly cloudy",
                3: "Overcast",
                45: "Fog",
                48: "Depositing rime fog",
                51: "Light drizzle",
                53: "Moderate drizzle",
                55: "Dense drizzle",
                61: "Slight rain",
                63: "Moderate rain",
                65: "Heavy rain",
                71: "Slight snow fall",
                73: "Moderate snow fall",
                75: "Heavy snow fall",
                77: "Snow grains",
                80: "Slight rain showers",
                81: "Moderate rain showers",
                82: "Violent rain showers",
                85: "Slight snow showers",
                86: "Heavy snow showers",
                95: "Thunderstorm",
                96: "Thunderstorm with slight hail",
                99: "Thunderstorm with heavy hail"
            }.get(weather_code, "Unknown weather condition")
            
            # Construct response
            text = f"Current weather: {weather_desc}, Temperature: {temperature}°C, Wind Speed: {windspeed} km/h"
            suggestions = [{"label": "View full forecast", "action": f"https://open-meteo.com/en/forecast?lat={lat}&lon={lon}"}]
            metadata = {"coordinates": [lat, lon], "type": "weather_info"}
            
            return AgentResponse(text=text, suggestions=suggestions, metadata=metadata).model_dump()
        
        except Exception as e:
            logger.error(f"Error in get_weather_info: {str(e)}")
            response = AgentResponse(
                text=f"Error fetching weather data: {str(e)}",
                suggestions=[],
                metadata={"error": str(e)}
            )
            return response.model_dump()