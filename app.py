# coordinator app.py

import sys
sys.path.append('.')
from flask import Flask, jsonify, request
import logging
from coordinator import Coordinator  # Assuming the Coordinator class is in coordinator.py

logging.basicConfig(level=logging.INFO)

app = Flask(__name__, static_folder='./static')

# Initialize the Coordinator with a list of node URLs
node_urls = ['http://192.168.1.110:5000', 'http://192.168.1.113:5000', 'http://192.168.1.119:5000']  # Example URLs of your LevelDB nodes
coordinator = Coordinator(node_urls=node_urls, cache_capacity=10, replicas=50)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/get/<key>', methods=['GET'])
def get_key(key):
    value = coordinator.get(key)
    if value is None:
        return jsonify({'error': 'Key not found'}), 404
    return jsonify({'key': key, 'value': value})

@app.route('/put', methods=['POST'])
def put_key():
    data = request.json
    key = data['key']
    value = data['value']
    coordinator.put(key, value)
    return jsonify({'key': key, 'value': value})

@app.route('/key-distribution', methods=['GET'])
def key_distribution():
    distribution = coordinator.get_key_distribution()
    return jsonify(distribution)

@app.route('/health', methods=['GET'])
def system_health():
    health_status = coordinator.check_health()
    return jsonify(health_status)

@app.route('/system-stats', methods=['GET'])
def system_stats():
    stats = coordinator.aggregate_stats()
    return jsonify(stats)

@app.route('/all', methods=['GET'])
def get_all():
    all_data = coordinator.get_all_key_values()
    return jsonify(all_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
