import requests
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class AgentResponse(BaseModel):
    text: str
    suggestions: List[Dict[str, str]]
    metadata: Dict[str, Any]

class ClimateImpactAgent:
    """Agent to fetch climate and weather information using coordinates."""
    
    def __init__(self):
        """Initialize the agent."""
        pass
    
    def get_weather_info(self, location: Optional[str] = "", coordinates: Optional[str] = None) -> dict:
        """
        Fetch weather information using coordinates.
        
        Args:
            location (Optional[str]): Optional name of the location.
            coordinates (Optional[str]): Coordinates in 'latitude,longitude' format.
        
        Returns:
            dict: Response containing text, suggestions, and metadata.
        """
        logger.info(f"Fetching location info for: {location}, Coordinates: {coordinates}. TOOL Calling for CLIAMTEImpactAgent")
        try:
            if not coordinates or not coordinates.strip():
                raise ValueError("Coordinates are required to fetch weather info.")
            
            lat_lon = coordinates.split(',')
            if len(lat_lon) != 2:
                raise ValueError("Coordinates must be in 'latitude,longitude' format.")
            
            try:
                lat, lon = float(lat_lon[0].strip()), float(lat_lon[1].strip())
            except ValueError:
                raise ValueError("Invalid coordinate values provided.")
            
            # Query weather data from Open-Meteo API using the coordinates
            url = (
                f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
                f"&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m"
                f"&daily=temperature_2m_max,temperature_2m_min,weather_code&timezone=auto"
            )
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            current = data.get('current', {})
            temperature = current.get('temperature_2m', 'Unknown')
            humidity = current.get('relative_humidity_2m', 'Unknown')
            windspeed = current.get('wind_speed_10m', 'Unknown')
            weather_code = current.get('weather_code', None)
            
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
            
            daily = data.get('daily', {})
            today_max = daily.get('temperature_2m_max', [None])[0]
            today_min = daily.get('temperature_2m_min', [None])[0]
            
            text = f"Current weather: {weather_desc}, Temperature: {temperature}°C"
            if today_min is not None and today_max is not None:
                text += f" (today's range: {today_min}°C to {today_max}°C)"
            text += f", Humidity: {humidity}%, Wind Speed: {windspeed} km/h."
            
            suggestions = [
                {"label": "View full forecast", "action": f"https://open-meteo.com/en/forecast?lat={lat}&lon={lon}"},
                {"label": "Check air quality", "action": "check_air_quality"},
                {"label": "View historical climate data", "action": "view_climate_history"}
            ]
            
            metadata = {
                "coordinates": f"{lat},{lon}",
                "location": location if location else f"Coordinates: {lat},{lon}",
                "type": "weather_info",
                "current": {
                    "temperature": temperature,
                    "weather_condition": weather_desc,
                    "humidity": humidity,
                    "wind_speed": windspeed
                },
                "daily": {
                    "max_temperature": today_max,
                    "min_temperature": today_min
                }
            }
            logger.info(f"Successfully fetched ClimateImpactAgent Data for: {location}, Coordinates: {coordinates}\ntext={text}\nSuggestions={suggestions}\nMetaData={metadata}")
            return AgentResponse(text=text, suggestions=suggestions, metadata=metadata).model_dump()
        
        except Exception as e:
            logger.error(f"Error in get_weather_info: {str(e)}")
            response = AgentResponse(
                text=f"Error fetching weather data: {str(e)}",
                suggestions=[],
                metadata={"error": str(e), "coordinates": coordinates}
            )
            return response.model_dump()
