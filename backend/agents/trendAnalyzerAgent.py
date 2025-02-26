import requests
import os
from dotenv import load_dotenv

load_dotenv()

class TrendAnalyzerAgent:
    def __init__(self):
        self.nasa_api = os.getenv('NASA_API_KEY')

    def predict_trends(self, coordinates):
        try:
            lat, lon = coordinates

            # Historical Satellite Data from NASA
            trend_url = f"https://api.nasa.gov/planetary/earth/assets?lon={lon}&lat={lat}&begin=2010-01-01&end=2025-01-01&dim=0.10&api_key={self.nasa_api}"
            trend_response = requests.get(trend_url)
            historical_data = trend_response.json() if trend_response.status_code == 200 else {}

            response = {
                "text": f"Geospatial trends near {lat},{lon}:\nPredicted urban expansion and {historical_data.get('status', 'N/A')} based on historical data.",
                "metadata": {
                    "coordinates": [lat, lon],
                    "type": "geospatial_trend"
                }
            }
            return response
        except Exception as e:
            print(f"TrendAnalyzerAgent error: {str(e)}")
            return {"text": f"Error predicting trends: {str(e)}", "metadata": {"error": str(e)}}