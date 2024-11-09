from geopy.geocoders import Nominatim

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
