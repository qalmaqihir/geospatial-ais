import requests
def validate_coordinates(lat, lon):
    try:
        lat, lon = float(lat), float(lon)
        return -90 <= lat <= 90 and -180 <= lon <= 180
    except ValueError:
        return False
    
def geocode_location(location):
    # Check if input is coordinates
    coord_match = re.match(r'^([-+]?\d+\.?\d*)[,\s]+([-+]?\d+\.?\d*)$', location)
    if coord_match:
        lat, lon = coord_match.groups()
        if validate_coordinates(lat, lon):
            return {'lat': float(lat), 'lon': float(lon)}
        raise ValueError('Invalid coordinates range')

    # Geocode via Nominatim
    try:
        response = requests.get(
            'https://nominatim.openstreetmap.org/search',
            params={'q': location, 'format': 'json', 'limit': 1, 'accept-language': 'en'},
            headers={'User-Agent': 'Geospatial-AI-App'},
            timeout=5
        )
        response.raise_for_status()
        data = response.json()
        if not data:
            raise ValueError('Location not found')
        return {'lat': float(data[0]['lat']), 'lon': float(data[0]['lon'])}
    except requests.RequestException as e:
        raise Exception(f'Geocoding service error: {str(e)}')