from flask import Flask, jsonify, request
from flask_cors import CORS
import usaddress
from agent import run_agent
from location import get_lat_long, get_address_from_lat_long

app = Flask(__name__)
CORS(app)

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
            elif apn:
                parsed_apn = usaddress.tag(apn)
                address = parsed_apn[0]
            elif lat and lon:
                location_dict = {
                    'location': get_address_from_lat_long(float(lat), float(lon)),
                    'latitude': float(lat),
                    'longitude': float(lon)
                }
                 
                 
            if location_dict:
                address = usaddress.tag(location_dict['location'])[0]

        print(address)
        if address:
            return run_agent(address)
        else:
            return jsonify({'message': f'No city found'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6969)
