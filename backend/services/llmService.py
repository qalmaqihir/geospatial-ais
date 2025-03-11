import os
import json
import logging
from dotenv import load_dotenv
from openai import OpenAI
import anthropic
import google.generativeai as genai
from typing import Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()

# Agents 
from agents.geoExplorerAgent import GeoExplorerAgent
from agents.climateImpactAgent import ClimateImpactAgent

# Instantiate the agents
geo_explorer = GeoExplorerAgent()
climate_impact = ClimateImpactAgent()

# Define tools for dynamic invocation
TOOL_CONFIG = {
    "geo_explorer": {
        "description": "Provides geographical information about a location.",
        "function": geo_explorer.get_location_info,
        "parameters": ["location", "coordinates"]
    },
    "climate_impact": {
        "description": "Provides climate and weather information for a location.",
        "function": climate_impact.get_weather_info,
        "parameters": ["location", "coordinates"]
    }
}


def get_llm_client(model: str) -> tuple:
    """Initialize and validate LLM clients with proper error handling."""
    try:
        if model == "gpt-4":
            client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            return client, "openai"
        elif model == "claude":
            return anthropic.Anthropic(api_key=os.getenv('CLAUDE_API_KEY')), "claude"
        elif model == "gemini":
            genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
            return genai.GenerativeModel('gemini-pro'), "gemini"
        elif model == "deepseek":
            client = OpenAI(
                api_key=os.getenv('DEEPSEEK_API_KEY'),
                base_url="https://api.deepseek.com/v1"
            )
            return client, "deepseek"
        raise ValueError(f"Unsupported model: {model}")
    except KeyError as e:
        logger.error(f"Missing API key: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Client initialization failed: {str(e)}")
        raise

def _format_llm_prompt(message: str, coordinates: Dict[str, Any], tools: dict) -> str:
    """Construct a structured prompt with strict JSON formatting requirements."""
    coord_text = f"at coordinates {coordinates['coordinates']} (zoom {coordinates['zoom']})" if coordinates else ""
    tool_descriptions = "\n".join(
        f"- {name}: {info['description']} (params: {info['parameters']})"
        for name, info in tools.items()
    )
    
    return f"""You are a geospatial AI assistant. The user is {coord_text} and asks: "{message}"

                Available Tools:
                {tool_descriptions}

                Response Requirements:
                1. If using a tool, output ONLY valid JSON with "tool" and "parameters"
                2. For direct answers, use JSON with "text" (natural language) and "suggestions"
                3. Maintain conversation flow and context

                Examples:
                Tool Call:
                {{
                "tool": "geo_explorer",
                "parameters": {{
                    "location": "Paris, France"
                }}
                }}

                Direct Response:
                {{
                "text": "Here's information about your location...",
                "suggestions": [
                    {{"label": "View Map", "action": "map:paris"}}
                ]
                }}"""

def _handle_tool_call(tool_name: str, parameters: dict) -> Dict[str, Any]:
    """Execute tool calls with proper validation and error handling."""
    try:
        if tool_name not in TOOL_CONFIG:
            return {"error": "Unknown tool", "details": tool_name}
        
        # Validate parameters
        required_params = TOOL_CONFIG[tool_name]["parameters"]
        missing = [p for p in required_params if p not in parameters]
        if missing:
            return {"error": "Missing parameters", "missing": missing}
        
        # Execute tool
        result = TOOL_CONFIG[tool_name]["function"](**parameters)
        
        # Convert tool-specific response to standard format
        return {
            "tool_response": result,
            "metadata": {
                "tool": tool_name,
                "success": "error" not in result
            }
        }
    except Exception as e:
        logger.error(f"Tool execution failed: {str(e)}")
        return {"error": "Tool execution failed", "details": str(e)}

def _generate_conversational_response(client, provider: str, model: str, user_query: str, tool_data: dict) -> Dict[str, Any]:
    """Convert raw tool data into a natural language response."""
    try:
        prompt = f"""Convert this technical data into a friendly, conversational response:
        
        User Query: {user_query}
        Tool Data: {json.dumps(tool_data, indent=2)}
        
        Guidelines:
        - Use simple, non-technical language
        - Highlight key information first
        - Include suggestions from the tool data
        - Acknowledge any data limitations
        - Keep responses under 3 paragraphs
        """
        
        if provider=="openai":
            response = client.chat.completions.create(
                model='gpt-4o-mini',
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that explains information clearly."},
                    {"role": "user", "content": prompt},
                ],
                response_format={"type": "json_object"},
                temperature=0.6
            )
            content = response.choices[0].message.content
        elif provider=="deepseek":
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that explains information clearly."},
                    {"role": "user", "content": prompt}
                ],
                stream=False
            )
            content = response.choices[0].message.content
        elif provider == "claude":
            response = client.messages.create(
                model='claude-3-opus-latest',
                max_tokens=400,
                messages=[{"role": "user", "content": prompt}]
            )
            content = response.content[0].text
        elif provider == "gemini-1.5-flash":
            response = client.generate_content(prompt)
            content = response.text
        
        return {
            "text": content,
            "suggestions": tool_data.get("suggestions", []),
            "analysis": tool_data.get("analysis", {})
        }
    except Exception as e:
        logger.error(f"Response generation failed: {str(e)}")
        return {"text": "I encountered an error processing that request. Please try again.", "error": str(e)}

def generate_llm_response(message: str, model: str, coordinates: Dict[str, Any]) -> Dict[str, Any]:
    """End-to-end processing with improved error handling and conversational flow."""
    try:
        client, provider = get_llm_client(model)
        prompt = _format_llm_prompt(message, coordinates, TOOL_CONFIG)
        
        # Get initial LLM response
        if provider=="openai":
            response = client.chat.completions.create(
                model='gpt-3.5-turbo',
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that explains information clearly."},
                    {"role": "user", "content": prompt},
                ],
                response_format={"type": "json_object"},
                temperature=0.6
            )
            llm_output = response.choices[0].message.content
        elif provider=="deepseek":
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that explains information clearly."},
                    {"role": "user", "content": prompt}
                ],
                stream=False
            )
            llm_output = response.choices[0].message.content
        elif provider == "claude":
            response = client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=400,
                messages=[{"role": "user", "content": prompt}]
            )
            llm_output = response.content[0].text
        elif provider == "gemini":
            response = client.generate_content(prompt)
            llm_output = response.text
        
        # Parse and validate response
        try:
            llm_response = json.loads(llm_output)
        except json.JSONDecodeError:
            logger.warning("Failed to parse LLM response as JSON, using fallback")
            return {
                "text": f"I'm having trouble processing that request. Here's what I can share: {llm_output}",
                "error": "Invalid JSON response"
            }

        # Process tool calls
        if "tool" in llm_response:
            tool_result = _handle_tool_call(llm_response["tool"], llm_response.get("parameters", {}))
            
            if "error" in tool_result:
                return _generate_conversational_response(
                    client, provider, model, message,
                    {"error": tool_result["error"], "original_query": message}
                )
            
            return _generate_conversational_response(
                client, provider, model, message,
                tool_result.get("tool_response", {})
            )

        # Direct response cleanup
        return {
            "text": llm_response.get("text", "I couldn't process that request."),
            "suggestions": llm_response.get("suggestions", []),
            "analysis": coordinates if coordinates else {}
        }

    except Exception as e:
        logger.error(f"End-to-end processing failed: {str(e)}")
        return {
            "text": "I'm having trouble with that request. Please try rephrasing or ask about something else.",
            "error": str(e)
        }


## TODO:
"""

Fix the initialization Error for the Gemini, Claude
:00] "POST /api/chat HTTP/1.1" 500 -
INFO:werkzeug:127.0.0.1 - - [11/Mar/2025 14:16:09] "OPTIONS /api/chat HTTP/1.1" 200 -
INFO:routes.chatRoutes:Chat request - Session: d10b5e85-2ad5-49bb-86ca-af9c0031c1b1, Model: gemmni
ERROR:services.llmService:Client initialization failed: Unsupported model: gemmni
ERROR:services.llmService:End-to-end processing failed: Unsupported model: gemmni
ERROR:routes.chatRoutes:LLM Error: Unsupported model: gemmni
INFO:werkzeug:127.0.0.1 - - [11/Mar/2025 14:16:09] "POST /api/chat HTTP/1.1" 500 -
INFO:werkzeug:127.0.0.1 - - [11/Mar/2025 14:16:19] "OPTIONS /api/chat HTTP/1.1" 200 -
INFO:routes.chatRoutes:Chat request - Session: d10b5e85-2ad5-49bb-86ca-af9c0031c1b1, Model: claude-2
ERROR:services.llmService:Client initialization failed: Unsupported model: claude-2
ERROR:services.llmService:End-to-end processing failed: Unsupported model: claude-2
ERROR:routes.chatRoutes:LLM Error: Unsupported model: claude-2



Check the Json Format error for G-P-T and DeepSeek
INFO:werkzeug:127.0.0.1 - - [11/Mar/2025 14:15:40] "OPTIONS /api/chat HTTP/1.1" 200 -
INFO:routes.chatRoutes:Chat request - Session: d10b5e85-2ad5-49bb-86ca-af9c0031c1b1, Model: deepseek
INFO:httpx:HTTP Request: POST https://api.deepseek.com/v1/chat/completions "HTTP/1.1 200 OK"
WARNING:services.llmService:Failed to parse LLM response as JSON, using fallback
ERROR:routes.chatRoutes:LLM Error: Invalid JSON response
INFO:werkzeug:127.0.0.1 - - [11/Mar/2025 14:15:49] "POST /api/chat HTTP/1.1" 500 -

INFO:werkzeug:127.0.0.1 - - [11/Mar/2025 14:15:58] "OPTIONS /api/chat HTTP/1.1" 200 -
INFO:routes.chatRoutes:Chat request - Session: d10b5e85-2ad5-49bb-86ca-af9c0031c1b1, Model: gpt-4
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 400 Bad Request"
ERROR:services.llmService:Response generation failed: Error code: 400 - {'error': {'message': "'messages' must contain the word 'json' in some form, to use 'response_format' of type 'json_object'.", 'type': 'invalid_request_error', 'param': 'messages', 'code': None}}
ERROR:routes.chatRoutes:LLM Error: Error code: 400 - {'error': {'message': "'messages' must contain the word 'json' in some form, to use 'response_format' of type 'json_object'.", 'type': 'invalid_request_error', 'param': 'messages', 'code': None}}
INFO:werkzeug:127.0.0.1 - - [11/Mar/2025 14:16:00] "POST /api/chat HTTP/1.1" 500 -

"""