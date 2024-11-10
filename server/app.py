from flask import Flask, jsonify, request, Response
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
    try:
        if request.method == 'GET':
            location = request.args.get('location')
            apn = request.args.get('apn')
            lat = request.args.get('lat')
            lon = request.args.get('lon')
            county = request.args.get('county')
            address = None
            location_dict = {}

            if location or apn or (lat and lon):
                if location:
                    lat_long = get_lat_long(location)
                    
                    if lat_long:
                        location_dict = {
                            'location': location,
                            'latitude': lat_long[0],
                            'longitude': lat_long[1],
                            'county': county
                        }
                        parsed_location = usaddress.tag(location)[0]
                        address = Address(
                            street_address=parsed_location.get('AddressNumber', '') + ' ' + 
                                         parsed_location.get('StreetName', '') + ' ' + 
                                         parsed_location.get('StreetNamePostType', ''),
                            city=parsed_location.get('PlaceName', ''),
                            state=parsed_location.get('StateName', ''),
                            zip_code=parsed_location.get('ZipCode', ''),
                            county=county  
                        )

            if address:
                return run_agent(address.model_dump(), location_dict)
            else:
                return jsonify({'message': 'No city found', 'error': False})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'An error occurred', 'error': True})

@app.route("/chat", methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get("message")
    history = data.get("history", [])
    
    completion = execute(message, history=history)
    
    response = {
        "message": completion.choices[0].message.content
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6969)
