import sys
sys.path.append('.')
import matplotlib.pyplot as plt
from coordinator import Coordinator

# Parameters
node_paths = ['node1', 'node2', 'node3', 'node4']
total_keys = 10
replication_factor = 2  # Ensure this is less than the total number of nodes

# Initialize Coordinator with replication
coordinator = Coordinator(node_paths=node_paths, cache_capacity=100, replicas=100, replication_factor=replication_factor)

# Setup Phase - Populate the system
for key in range(total_keys):
    coordinator.put(str(key), f"value-{key}")

def test_key_retrievals():
    successful_retrievals = 0
    for key in range(total_keys):
        if coordinator.get(str(key)) is not None:
            successful_retrievals += 1
    return successful_retrievals

# Test replication validity
def verify_replication():
    for key in range(total_keys):
        primary_node = coordinator.get_node(str(key))
        replication_nodes = coordinator._get_replication_nodes(primary_node, str(key))
        if not replication_nodes or primary_node not in replication_nodes:
            print(f"Data for key {key} is not replicated correctly.")
            return False
    return True

# Verify initial replication
assert verify_replication(), "Initial replication failed"

# Action and Measurement Phase
initial_success = test_key_retrievals()
print(f"Initial success rate (no failures): {initial_success / total_keys}")

success_rates = [initial_success / total_keys]
failed_nodes = []

for node_path in node_paths[:-1]:  # Leave one node to ensure data is still accessible
    coordinator.remove_node(node_path)
    failed_nodes.append(node_path)
    print(f"Removed node {node_path}. Testing retrieval...")

    success_rate = test_key_retrievals() / total_keys
    success_rates.append(success_rate)

    print(f"Success rate after failing {len(failed_nodes)} nodes: {success_rate}")

# Output Phase - Graph the success rate
plt.figure(figsize=(10, 6))
plt.plot(range(len(success_rates)), success_rates, marker='o', linestyle='-')
plt.title("Success Rate of Key Retrievals vs. Number of Node Failures")
plt.xlabel("Number of Node Failures")
plt.ylabel("Success Rate")
plt.xticks(range(len(success_rates)), labels=[f"{i}" for i in range(len(success_rates))])
plt.grid(True)
plt.show()
