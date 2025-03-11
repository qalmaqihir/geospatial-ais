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
CORS(app, supports_credentials=True)  # Allow credentials (cookies)

# Session configuration
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
if not app.config['SECRET_KEY']:
    raise ValueError("SECRET_KEY must be set in environment variables")
Session(app)

# Rate limiting
limiter = Limiter(app=app, key_func=get_remote_address, default_limits=['200 per day', '50 per hour'])

# Register blueprints
app.register_blueprint(map_bp, url_prefix='/api')
app.register_blueprint(chat_bp, url_prefix='/api')
app.register_blueprint(health_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_ENV') != 'production', host='0.0.0.0', port=5000)