from geopy.geocoders import Nominatim
import requests

def get_lat_long(address):
    geolocator = Nominatim(user_agent="fintech hackathon")
    location = geolocator.geocode(address)

    if location:
        return (location.latitude, location.longitude)
    else:
        return None

def get_address_from_lat_long(latitude, longitude):
    geolocator = Nominatim(user_agent="fintech hackathon")
    location = geolocator.reverse((latitude, longitude))
    
    if location:
        return location.address
    else:
        return "Address not found."

def get_county_from_coordinates(latitude: float, longitude: float) -> str:
    try:
        url = f"https://geocoding.geo.census.gov/geocoder/geographies/coordinates"
        
        params = {
            "x": longitude,
            "y": latitude,
            "benchmark": "Public_AR_Current",
            "vintage": "Current_Current",
            "format": "json"
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status() 
        
        data = response.json()
        
        result = data.get("result", {})
        geographies = result.get("geographies", {})
        counties = geographies.get("Counties", [])
        
        if counties and len(counties) > 0:
            return counties[0].get("NAME", "").replace(" County", "")
            
        return ""
        
    except Exception as e:
        print(f"Error getting county from coordinates: {e}")
        return ""
