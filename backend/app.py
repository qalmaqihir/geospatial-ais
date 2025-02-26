# # from flask import Flask, jsonify, request
# # from flask_cors import CORS
# # import requests
# # from dotenv import load_dotenv
# # import os
# # import re
# # from flask_limiter import Limiter
# # from flask_limiter.util import get_remote_address
# # from flask_session import Session



# # load_dotenv()

# # app = Flask(__name__)
# # CORS(app)


# # # Rate limiting setup
# # limiter = Limiter(
# #     app=app,
# #     key_func=get_remote_address,
# #     default_limits=["200 per day", "50 per hour"]
# # )

# # # Session configuration
# # app.config["SESSION_TYPE"] = "filesystem"
# # app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
# # app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "default_secret_key")
# # Session(app)



# # def validate_coordinates(lat, lon):
# #     try:
# #         lat = float(lat)
# #         lon = float(lon)
# #         return -90 <= lat <= 90 and -180 <= lon <= 180
# #     except ValueError:
# #         return False

# # # Enhanced geocode endpoint
# # @app.route('/geocode')
# # @limiter.limit("10 per minute")

# # # @app.route('/geocode')
# # def geocode():
# #     location = request.args.get('location')
# #     if not location:
# #         return jsonify({'error': 'Missing location parameter'}), 400
    
# #     # Check if input is coordinates
# #     coord_match = re.match(r'^([-+]?\d+\.?\d*)[,\s]+([-+]?\d+\.?\d*)$', location)
# #     if coord_match:
# #         lat, lon = coord_match.groups()
# #         if validate_coordinates(lat, lon):
# #             return jsonify({'lat': float(lat), 'lon': float(lon)})
# #         return jsonify({'error': 'Invalid coordinates range'}), 400

# #     try:
# #         response = requests.get(
# #             'https://nominatim.openstreetmap.org/search',
# #             params={
# #                 'q': location,
# #                 'format': 'json',
# #                 'limit': 1,
# #                 'accept-language': 'en'
# #             },
# #             headers={'User-Agent': 'Geospatial-AI-App'}
# #         )
# #         response.raise_for_status()
# #         data = response.json()
        
# #         if not data:
# #             return jsonify({'error': 'Location not found'}), 404
            
# #         return jsonify({
# #             'lat': float(data[0]['lat']),
# #             'lon': float(data[0]['lon'])
# #         })
        
# #     except requests.exceptions.RequestException as e:
# #         return jsonify({'error': f'Geocoding service error: {str(e)}'}), 500
# #     except Exception as e:
# #         return jsonify({'error': f'Unexpected error: {str(e)}'}), 500
    

# # @app.route('/chat', methods=['POST'])
# # def chat():
# #     session_id = request.cookies.get("session_id")
# #     data = request.get_json()
    
# #     # Basic session validation
# #     if not session_id:
# #         return jsonify({"error": "Invalid session"}), 401
        
# #     # Mock LLM response
# #     response = {
# #         "text": f"Mock response from {data['model']}: {data['message']}",
# #         "analysis": {
# #             "coordinates": data.get("coordinates"),
# #             "visualization": "heatmap"
# #         }
# #     }
    
# #     return jsonify(response)

# # @app.route('/session', methods=['POST'])
# # def create_session():
# #     session["initialized"] = True
# #     return jsonify({"message": "Session initialized"})


# # # Pseudo-code for LLM integration
# # # def generate_llm_response(message, context):
# # #     if "climate" in message:
# # #         return climate_analysis(context['coordinates'])
# # #     elif "visualize" in message:
# # #         return visualization_suggestion(context['area'])
# # #     # Add more domain-specific handlers


# # if __name__ == '__main__':
# #     app.run(debug=True)


# from flask import Flask
# from flask_cors import CORS
# from flask_session import Session
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address
# from dotenv import load_dotenv
# import os
# from routes.mapRoutes import map_bp
# from routes.chatRoutes import chat_bp
# from routes.healthRoutes import health_bp

# load_dotenv()

# app = Flask(__name__)
# CORS(app)

# # Session configuration
# app.config['SESSION_TYPE'] = 'filesystem'
# app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
# app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
# Session(app)

# # Rate limiting
# limiter = Limiter(app=app, key_func=get_remote_address, default_limits=['200 per day', '50 per hour'])

# # Register blueprints
# app.register_blueprint(map_bp, url_prefix='/api')
# app.register_blueprint(chat_bp, url_prefix='/api')
# app.register_blueprint(health_bp, url_prefix='/api')

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)

# from flask import Flask
# from flask_cors import CORS
# from flask_session import Session
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address
# from dotenv import load_dotenv
# import os
# from routes.mapRoutes import map_bp
# from routes.chatRoutes import chat_bp
# from routes.healthRoutes import health_bp

# load_dotenv()

# app = Flask(__name__)
# CORS(app, supports_credentials=True)  # Allow credentials (cookies)

# # Session configuration
# app.config['SESSION_TYPE'] = 'filesystem'
# app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
# app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
# Session(app)

# # Rate limiting
# limiter = Limiter(app=app, key_func=get_remote_address, default_limits=['200 per day', '50 per hour'])

# # Register blueprints
# app.register_blueprint(map_bp, url_prefix='/api')
# app.register_blueprint(chat_bp, url_prefix='/api')
# app.register_blueprint(health_bp, url_prefix='/api')

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)

from flask import Flask
from flask_cors import CORS
from flask_session import Session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
import os
from routes.mapRoutes import map_bp
from routes.chatRoutes import chat_bp
from routes.healthRoutes import health_bp

load_dotenv()

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=['http://localhost:3000'])  # Match frontend origin

# Session configuration
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
Session(app)

# Rate limiting
limiter = Limiter(app=app, key_func=get_remote_address, default_limits=['200 per day', '50 per hour'])

# Register blueprints
app.register_blueprint(map_bp, url_prefix='/api')
app.register_blueprint(chat_bp, url_prefix='/api')
app.register_blueprint(health_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)