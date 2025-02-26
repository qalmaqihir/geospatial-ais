from flask import Blueprint, jsonify, request
from services.geocodingService import geocode_location
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

map_bp = Blueprint('map', __name__)
limiter = Limiter(app=None, key_func=get_remote_address)

@map_bp.route('/geocode', methods=['GET'])
@limiter.limit('10 per minute')
def geocode():
    location = request.args.get('location')
    if not location:
        return jsonify({'error': 'Missing location parameter'}), 400

    try:
        result = geocode_location(location)
        return jsonify(result)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Geocoding failed: {str(e)}'}), 500