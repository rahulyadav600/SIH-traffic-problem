from flask import Flask, request, jsonify
from flask_cors import CORS
import threading, time

app = Flask(__name__)
CORS(app)

# Global traffic data
traffic_data = {"NORTH": 0, "SOUTH": 0, "EAST": 0, "WEST": 0}
lock = threading.Lock()

@app.route('/update_traffic', methods=['POST'])
def update_traffic():
    data = request.get_json(force=True)
    direction = data.get('direction')
    count = int(data.get('count', 0))

    if direction not in traffic_data:
        return jsonify({'error': 'Invalid direction'}), 400

    with lock:
        traffic_data[direction] = count
    return jsonify({'status': 'ok', 'traffic': traffic_data}), 200

@app.route('/get_status', methods=['GET'])
def get_status():
    with lock:
        green = max(traffic_data, key=traffic_data.get)
        return jsonify({'green_signal': green, 'traffic': traffic_data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
