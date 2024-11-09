from flask import Flask, jsonify, request
from flask_cors import CORS
from pydantic import BaseModel
import usaddress
from agent import run_agent
from location import get_lat_long, get_address_from_lat_long
from ai import execute

app = Flask(__name__)
CORS(app)

class Address(BaseModel):
    street_address: str
    city: str
    state: str
    zip_code: str
    county: str

@app.route('/', methods=['GET'])
def hello_world():
    if request.method == 'GET':
        location = request.args.get('location')
        apn = request.args.get('apn')
        lat = request.args.get('lat')
        lon = request.args.get('lon')
        address = None
        location_dict = {}

        if location or apn or (lat and lon):
            if location:
                lat_long = get_lat_long(location)
                
                if lat_long:
                    location_dict = {
                        'location': location,
                        'latitude': lat_long[0],
                        'longitude': lat_long[1]
                    }
                    parsed_location = usaddress.tag(location)[0]
                    address = Address(
                        street_address=parsed_location.get('AddressNumber', '') + ' ' + 
                                     parsed_location.get('StreetName', '') + ' ' + 
                                     parsed_location.get('StreetNamePostType', ''),
                        city=parsed_location.get('PlaceName', ''),
                        state=parsed_location.get('StateName', ''),
                        zip_code=parsed_location.get('ZipCode', ''),
                        county=''  
                    )
            elif apn:
                parsed_apn = usaddress.tag(apn)[0]
                address = Address(
                    street_address=parsed_apn.get('AddressNumber', '') + ' ' + 
                                 parsed_apn.get('StreetName', '') + ' ' + 
                                 parsed_apn.get('StreetNamePostType', ''),
                    city=parsed_apn.get('PlaceName', ''),
                    state=parsed_apn.get('StateName', ''),
                    zip_code=parsed_apn.get('ZipCode', ''),
                    county=''
                )
            elif lat and lon:
                address_str = get_address_from_lat_long(float(lat), float(lon))
                if address_str:
                    location_dict = {
                        'location': address_str,
                        'latitude': float(lat),
                        'longitude': float(lon)
                    }
                    
                    address = execute("What is the address for this location? " + location_dict['location'], 
                                   response_format=Address)

        print("location_dict", location_dict)
        if address:
            return run_agent(address.model_dump(), location_dict)
        else:
            return jsonify({'message': f'No city found'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6969)
