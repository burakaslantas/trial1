import sys
sys.path.append('.')
import matplotlib.pyplot as plt
from coordinator import Coordinator

# Assuming you have the Coordinator class defined and imported
# Initialize the Coordinator with a set of node paths
node_paths = ['node1', 'node2', 'node3', 'node4']  # Adjust as per your setup
replication_factor = 2  # Adjust based on your needs

coordinator = Coordinator(node_paths=node_paths, cache_capacity=100, replicas=100, replication_factor=replication_factor)

# Now, we can test the put and replication logic
key = "0"
value = "0"
primary_node = coordinator.get_node(key)
coordinator.put(key, value)

# Check if the key is replicated correctly
replication_nodes = coordinator._get_replication_nodes(primary_node, key)
assert len(replication_nodes) == replication_factor - 1, "Incorrect number of replication nodes"

for node_path in replication_nodes:
    node = coordinator.nodes[node_path]
    replicated_value = node.get(key)
    assert replicated_value == value, f"Replication failed for key {key} on node {node_path}"

print("Replication test passed successfully.")
