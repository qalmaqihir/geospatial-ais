import os
import json
import re
import logging
from dotenv import load_dotenv
from openai import OpenAI
from typing import Dict, Any, List, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()

# Agents 
from agents.geoExplorerAgent import GeoExplorerAgent
from agents.climateImpactAgent import ClimateImpactAgent
from agents.infoAgent import InfoAgent
from utils.geoUtils import geocode_location, reverse_geocode

# Instantiate the agents
geo_explorer = GeoExplorerAgent()
climate_impact = ClimateImpactAgent()
info_agent = InfoAgent()

# Define tools for OpenAI tool calling format with strict mode.
# Note: reverse_geocode is used internally and not exposed as a tool.
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "geo_explorer",
            "description": "Provides detailed geographical information about a location including coordinates, administrative regions, population, and landmarks.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "nullable": True,
                        "description": "The name of the location (e.g., 'Paris, France')."
                    },
                    "coordinates": {
                        "type": "string",
                        "nullable": True,
                        "description": "Coordinates in 'latitude,longitude' format (e.g., '48.8566,2.3522')."
                    }
                },
                "required": ["location", "coordinates"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "climate_impact",
            "description": "Provides detailed climate and weather information for a location including current conditions, forecasts, and historical climate data.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "nullable": True,
                        "description": "The name of the location (e.g., 'New York, USA')."
                    },
                    "coordinates": {
                        "type": "string",
                        "nullable": True,
                        "description": "Coordinates in 'latitude,longitude' format (e.g., '40.7128,-74.0060')."
                    }
                },
                "required": ["location", "coordinates"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "info_agent",
            "description": "Provides detailed regional information (history, culture, and cuisine) for a location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "nullable": True,
                        "description": "The name of the region (e.g., 'Rawalpindi')."
                    },
                    "coordinates": {
                        "type": "string",
                        "nullable": True,
                        "description": "Coordinates in 'latitude,longitude' format."
                    }
                },
                "required": ["location", "coordinates"],
                "additionalProperties": False
            },
            "strict": True
        }
    }
]

# Function mapping for execution.
TOOL_FUNCTIONS = {
    "geo_explorer": geo_explorer.get_location_info,
    "climate_impact": climate_impact.get_weather_info,
    "info_agent": info_agent.get_info
}

def get_openai_client() -> OpenAI:
    """Initialize and validate OpenAI client with proper error handling."""
    try:
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        return client
    except KeyError as e:
        logger.error(f"Missing API key: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Client initialization failed: {str(e)}")
        raise

def execute_tool_calls(tool_calls: List[Dict], messages: List[Dict], default_location: Optional[str] = None) -> List[Dict]:
    """
    Execute tool calls and append the results to the conversation history.
    If a tool call for geo_explorer, climate_impact, or info_agent is missing the "location" parameter,
    it is filled in with default_location.
    """
    if not tool_calls:
        return messages
        
    for tool_call in tool_calls:
        try:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            if function_name in ["geo_explorer", "climate_impact", "info_agent"]:
                if "location" not in function_args or not function_args["location"]:
                    function_args["location"] = default_location if default_location is not None else ""
            
            if function_name not in TOOL_FUNCTIONS:
                tool_result = json.dumps({"error": f"Unknown function: {function_name}"})
            else:
                result = TOOL_FUNCTIONS[function_name](**function_args)
                tool_result = json.dumps(result)
                
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": tool_result
            })
            
        except Exception as e:
            logger.error(f"Error executing function {function_name}: {str(e)}")
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps({"error": str(e)})
            })
            
    return messages

def refine_response(client: OpenAI, technical_response: str) -> str:
    """
    Convert a technical response into a friendly, conversational answer with suggestions and links.
    """
    refine_prompt = f"""Please convert the following technical response into a friendly, concise, and conversational answer.
Include helpful suggestions and relevant links for further exploration, but avoid unnecessary technical details.

Response:
{technical_response}"""
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a friendly assistant that reformats technical content into engaging, easy-to-understand language with suggestions and links."},
            {"role": "user", "content": refine_prompt}
        ],
        temperature=0.7
    )
    refined = response.choices[0].message.content
    return refined

def generate_llm_response(message: str, coordinates: Optional[Dict[str, Any]] = None, model: str = "gpt-4o") -> Dict[str, Any]:
    """
    End-to-end processing with tool calling. Resolves the location name using coordinates,
    injects it into the system prompt, processes tool calls, and finally refines the output
    into a friendly and informative response.
    
    Args:
        message: User's query text.
        coordinates: Optional location details, e.g., {"coordinates": {"coordinates": [lat,lon], "zoom": zoom_level}}.
        model: OpenAI model to use.
    
    Returns:
        A dict containing the final refined response text and additional metadata.
    """
    try:
        client = get_openai_client()
        
        # Resolve the location name from the coordinates.
        location_name = "Unknown location"
        if coordinates and "coordinates" in coordinates:
            coord_value = coordinates['coordinates']['coordinates']
            if isinstance(coord_value, list):
                coord_str = ",".join(map(str, coord_value))
            else:
                coord_str = str(coord_value)
            try:
                lat_str, lon_str = coord_str.split(",")
                lat, lon = float(lat_str.strip()), float(lon_str.strip())
                location_name = reverse_geocode(lat, lon)
                logger.info(f"Reverse geocoded location: {location_name}")
            except Exception as e:
                logger.warning(f"Failed to reverse geocode coordinates: {e}")
        
        # Create system message with instructions.
        coord_text = f"at coordinates {coordinates['coordinates']['coordinates']} (zoom {coordinates['zoom']})" if coordinates else ""
        system_message = f"""You are a geospatial AI assistant specialized in providing friendly, concise, and useful location-based information.
The user is located in '{location_name}' {coord_text}.

When responding, please:
- Provide clear, succinct answers.
- Include helpful suggestions and links where relevant.
- Focus on delivering the most important information first.
- Use a friendly and conversational tone.

Use the geo_explorer tool for geographical details, the climate_impact tool for weather data, and the info_agent tool for regional history, culture, and cuisine.
If you can answer directly, avoid unnecessary technical details."""
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": message}
        ]
        
        # First API call: Get the initial response with potential tool calls.
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0.7
        )
        
        response_message = response.choices[0].message
        
        # Append the assistant's response, preserving any tool_calls.
        if hasattr(response_message, "tool_calls") and response_message.tool_calls:
            messages.append({
                "role": response_message.role,
                "content": response_message.content or "",
                "tool_calls": response_message.tool_calls
            })
        else:
            messages.append({"role": response_message.role, "content": response_message.content or ""})
        
        # If tool calls are present, execute them.
        if hasattr(response_message, "tool_calls") and response_message.tool_calls:
            messages = execute_tool_calls(response_message.tool_calls, messages, default_location=location_name)
            
            # Make a second API call with the updated conversation history.
            final_response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7
            )
            
            final_message = final_response.choices[0].message
        else:
            final_message = response_message
        
        # Refine the final technical response into a friendly, informative answer.
        refined_text = refine_response(client, final_message.content)
        
        return {
            "text": refined_text,
            "tool_usage": [t.function.name for t in response_message.tool_calls] if hasattr(response_message, "tool_calls") and response_message.tool_calls else [],
            "analysis": coordinates if coordinates else {}
        }
    
    except Exception as e:
        logger.error(f"End-to-end processing failed: {str(e)}")
        return {
            "text": "I'm having trouble with that request. Please try rephrasing or ask about something else.",
            "error": str(e)
        }
