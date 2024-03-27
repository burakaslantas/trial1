from flask import Flask, render_template
import json
from coordinator import Coordinator

app = Flask(__name__)

# Assuming coordinator is an instance of your Coordinator class
coordinator = Coordinator(['node1', 'node2', 'node3'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/nodes')
def nodes():
    nodes_data = {path: list(node.db) for path, node in coordinator.nodes.items()}
    return json.dumps(nodes_data)

@app.route('/cache')
def cache():
    cache_data = {node.key: node.value for node in coordinator.cache.cache.values()}
    return json.dumps(cache_data)

@app.route('/ring')
def ring():
    ring_data = list(coordinator.hashing.ring.items())
    return json.dumps(ring_data)

if __name__ == '__main__':
    app.run(debug=True)
