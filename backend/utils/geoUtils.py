import requests
import re
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


def reverse_geocode(lat, lon):
    """
    Reverse geocode latitude and longitude to a human-readable location name.
    
    Args:
        lat (float): Latitude.
        lon (float): Longitude.
    
    Returns:
        str: The display name of the location (e.g., "Paris, Île-de-France, France").
    
    Raises:
        ValueError: If coordinates are invalid or no location is found.
        Exception: If there is a reverse geocoding service error.
    """
    if not validate_coordinates(lat, lon):
        raise ValueError('Invalid coordinates')

    try:
        response = requests.get(
            'https://nominatim.openstreetmap.org/reverse',
            params={'lat': lat, 'lon': lon, 'format': 'json', 'accept-language': 'en'},
            headers={'User-Agent': 'Geospatial-AI-App'},
            timeout=5
        )
        response.raise_for_status()
        data = response.json()
        if 'display_name' in data:
            return data['display_name']
        else:
            raise ValueError('No location found for the given coordinates')
    except requests.RequestException as e:
        raise Exception(f'Reverse geocoding service error: {str(e)}')

# # Example usage for testing
# if __name__ == "__main__":
#     print("Geocoding 'Paris':", geocode_location("Paris"))
#     print("Reverse geocoding (48.8566, 2.3522):", reverse_geocode(48.8566, 2.3522))