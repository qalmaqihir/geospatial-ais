from openai import OpenAI
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def generate_llm_response(message, model, coordinates):
    try:
        logger.debug(f"Received message: {message}, model: {model}, coordinates: {coordinates}")
        if not os.getenv('OPENAI_API_KEY'):
            raise ValueError("OpenAI API key is not set in environment variables")

        coords = coordinates.get('coordinates', 'unknown') if coordinates else 'unknown'
        zoom = coordinates.get('zoom', 'unknown') if coordinates else 'unknown'
        prompt = f"""You are a geospatial AI assistant. The user is at coordinates {coords} with zoom level {zoom}. They asked: "{message}". Provide a helpful response in JSON format with 'text' and 'suggestions' fields. Suggestions should be actionable (e.g., URLs or commands) related to the query. Example:
        {{
          "text": "Here are some tourist attractions near you.",
          "suggestions": [
            {{"label": "Visit Eiffel Tower", "action": "https://www.toureiffel.paris/en"}},
            {{"label": "Explore Louvre", "action": "https://www.louvre.fr/en"}}
          ]
        }}"""

        response = client.chat.completions.create(
            model=model if model in ['gpt-4', 'gpt-3.5-turbo'] else 'gpt-3.5-turbo',
            messages=[
                {"role": "system", "content": "You are a helpful geospatial AI assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7
        )

        json_response = eval(response.choices[0].message.content)  # Parse JSON (unsafe, replace with json.loads later)
        logger.debug(f"OpenAI response: {json_response}")
        
        return {
            'text': json_response['text'],
            'suggestions': json_response.get('suggestions', []),
            'analysis': {'coordinates': coords, 'visualization': 'heatmap' if 'density' in message.lower() else None}
        }
    except Exception as e:
        logger.error(f"LLM request failed: {str(e)}")
        raise Exception(f"LLM request failed: {str(e)}")



# from openai import OpenAI
# import os
# from dotenv import load_dotenv
# import logging
# from agents.geoExplorerAgent import GeoExplorerAgent
# from agents.visualGuideAgent import VisualGuideAgent
# from agents.climateImpactAgent import ClimateImpactAgent
# from agents.travelPlannerAgent import TravelPlannerAgent
# from agents.disasterRiskAgent import DisasterRiskAgent
# from agents.deepSeaAgent import DeepSeaAgent
# from agents.historicalTimeMachineAgent import HistoricalTimeMachineAgent
# from agents.ecoFootprintAgent import EcoFootprintAgent
# from agents.cultureLanguageAgent import CultureLanguageAgent
# from agents.trendAnalyzerAgent import TrendAnalyzerAgent

# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)

# load_dotenv()

# client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# # Initialize agents
# geo_explorer = GeoExplorerAgent()
# visual_guide = VisualGuideAgent()
# climate_impact = ClimateImpactAgent()
# travel_planner = TravelPlannerAgent()
# disaster_risk = DisasterRiskAgent()
# deep_sea = DeepSeaAgent()
# historical_time = HistoricalTimeMachineAgent()
# eco_footprint = EcoFootprintAgent()
# culture_language = CultureLanguageAgent()
# trend_analyzer = TrendAnalyzerAgent()

# def generate_llm_response(message, model, coordinates):
#     try:
#         if not os.getenv('OPENAI_API_KEY'):
#             raise ValueError("OpenAI API key is not set in environment variables")

#         coords = coordinates.get('coordinates', 'unknown') if coordinates else 'unknown'
#         zoom = coordinates.get('zoom', 'unknown') if coordinates else 'unknown'
#         selected_area = coordinates.get('selectedArea', None)

#         # Define functions for OpenAI to call
#         functions = [
#             {
#                 "name": "get_location_info",
#                 "description": "Fetch real-time and historical info about a location",
#                 "parameters": {
#                     "type": "object",
#                     "properties": {
#                         "location": {"type": "string"},
#                         "coordinates": {"type": "array", "items": {"type": "number"}}
#                     },
#                     "required": ["coordinates"]
#                 }
#             },
#             {
#                 "name": "get_visual_data",
#                 "description": "Fetch visual data (images, satellite views) for a location",
#                 "parameters": {
#                     "type": "object",
#                     "properties": {
#                         "coordinates": {"type": "array", "items": {"type": "number"}}
#                     },
#                     "required": ["coordinates"]
#                 }
#             },
#             # Add similar function definitions for other agents...
#             {
#                 "name": "analyze_climate_impact",
#                 "description": "Analyze climate changes for a location",
#                 "parameters": {
#                     "type": "object",
#                     "properties": {
#                         "coordinates": {"type": "array", "items": {"type": "number"}}
#                     },
#                     "required": ["coordinates"]
#                 }
#             },
#             {
#                 "name": "plan_travel",
#                 "description": "Suggest travel plans and attractions for a location",
#                 "parameters": {
#                     "type": "object",
#                     "properties": {
#                         "coordinates": {"type": "array", "items": {"type": "number"}},
#                         "query": {"type": "string"}
#                     },
#                     "required": ["coordinates"]
#                 }
#             },
#             {
#                 "name": "assess_disaster_risk",
#                 "description": "Assess natural disaster risks for a location",
#                 "parameters": {
#                     "type": "object",
#                     "properties": {
#                         "coordinates": {"type": "array", "items": {"type": "number"}}
#                     },
#                     "required": ["coordinates"]
#                 }
#             },
#             {
#                 "name": "analyze_deep_sea",
#                 "description": "Provide marine intelligence for ocean areas",
#                 "parameters": {
#                     "type": "object",
#                     "properties": {
#                         "coordinates": {"type": "array", "items": {"type": "number"}}
#                     },
#                     "required": ["coordinates"]
#                 }
#             },
#             {
#                 "name": "get_historical_data",
#                 "description": "Fetch historical maps and data for a location",
#                 "parameters": {
#                     "type": "object",
#                     "properties": {
#                         "coordinates": {"type": "array", "items": {"type": "number"}}
#                     },
#                     "required": ["coordinates"]
#                 }
#             },
#             {
#                 "name": "analyze_eco_footprint",
#                 "description": "Analyze carbon footprint and environmental impact",
#                 "parameters": {
#                     "type": "object",
#                     "properties": {
#                         "coordinates": {"type": "array", "items": {"type": "number"}}
#                     },
#                     "required": ["coordinates"]
#                 }
#             },
#             {
#                 "name": "get_cultural_insights",
#                 "description": "Provide local culture and language insights",
#                 "parameters": {
#                     "type": "object",
#                     "properties": {
#                         "coordinates": {"type": "array", "items": {"type": "number"}}
#                     },
#                     "required": ["coordinates"]
#                 }
#             },
#             {
#                 "name": "predict_trends",
#                 "description": "Predict geospatial trends like urban expansion",
#                 "parameters": {
#                     "type": "object",
#                     "properties": {
#                         "coordinates": {"type": "array", "items": {"type": "number"}}
#                     },
#                     "required": ["coordinates"]
#                 }
#             }
#         ]

#         # Call OpenAI with function calling
#         response = client.chat.completions.create(
#             model=model if model in ['gpt-4', 'gpt-3.5-turbo'] else 'gpt-3.5-turbo',
#             messages=[
#                 {"role": "system", "content": "You are a geospatial AI assistant that uses function calls to fetch detailed information."},
#                 {"role": "user", "content": message}
#             ],
#             functions=functions,
#             function_call="auto"
#         )

#         # Handle function call
#         response_message = response.choices[0].message
#         if response_message.function_call:
#             function_name = response_message.function_call.name
#             function_args = eval(response_message.function_call.arguments)  # Parse JSON (replace with json.loads for safety)

#             if function_name == "get_location_info":
#                 return geo_explorer.get_location_info(None, function_args.get('coordinates'))
#             elif function_name == "get_visual_data":
#                 return visual_guide.get_visual_data(function_args['coordinates'])
#             elif function_name == "analyze_climate_impact":
#                 return climate_impact.analyze_climate_impact(function_args['coordinates'])
#             elif function_name == "plan_travel":
#                 return travel_planner.plan_travel(function_args['coordinates'], function_args.get('query'))
#             elif function_name == "assess_disaster_risk":
#                 return disaster_risk.assess_disaster_risk(function_args['coordinates'])
#             elif function_name == "analyze_deep_sea":
#                 return deep_sea.analyze_deep_sea(function_args['coordinates'])
#             elif function_name == "get_historical_data":
#                 return historical_time.get_historical_data(function_args['coordinates'])
#             elif function_name == "analyze_eco_footprint":
#                 return eco_footprint.analyze_eco_footprint(function_args['coordinates'])
#             elif function_name == "get_cultural_insights":
#                 return culture_language.get_cultural_insights(function_args['coordinates'])
#             elif function_name == "predict_trends":
#                 return trend_analyzer.predict_trends(function_args['coordinates'])
#             else:
#                 return {"text": "Unknown function call", "metadata": {"error": "Invalid function"}}

#         return {
#             "text": response_message.content or "No response generated.",
#             "metadata": {"coordinates": coords, "type": "default"}
#         }
#     except Exception as e:
#         logger.error(f"LLM request failed: {str(e)}")
#         raise Exception(f"LLM request failed: {str(e)}")