from flask import Flask, jsonify, request
from flask_cors import CORS
import usaddress
from agent import run_agent

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def hello_world():
    if request.method == 'GET':
        location = request.args.get('location', 'World')
        parsed = usaddress.tag(location)
        address = parsed[0]
        
        if address['PlaceName']:
            return run_agent(address)
        else:
            return jsonify({'message': f'No city found'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6969)
