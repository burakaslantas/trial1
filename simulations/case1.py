"""
########################################################
Simulation Case 1: Load Distribution Analysis
########################################################

Objective: To visualize how keys are distributed across the nodes in your distributed key-value store.

Parameters to Input:
    * Number of nodes
    * Number of keys to insert
    * Number of replicas per node

Expected Output:
    * A histogram showing the number of keys managed by each node.
"""
import sys
sys.path.append('.')
import matplotlib.pyplot as plt
from consistent_hashing import ConsistentHashing
import hashlib

def simulate_load_distribution(num_nodes, num_keys, replicas):
    # Initialize consistent hashing with specified number of replicas
    hashing = ConsistentHashing(replicas=replicas)
    
    # Add nodes to the ring
    for i in range(num_nodes):
        node_name = f'node_{i}'
        hashing.add_node(node_name)
    
    # Simulate inserting keys and track how many keys each node gets
    node_distribution = {f'node_{i}': 0 for i in range(num_nodes)}
    for i in range(num_keys):
        key = f'key_{i}'
        node = hashing.get_node(key)
        node_distribution[node] += 1
    
    # Plotting
    nodes = list(node_distribution.keys())
    keys_per_node = list(node_distribution.values())
    
    plt.figure(figsize=(10, 6))
    plt.bar(nodes, keys_per_node, color='skyblue')
    plt.xlabel('Nodes')
    plt.ylabel('Number of Keys')
    plt.title('Load Distribution Across Nodes')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Input parameters
num_nodes = int(input("Enter the number of nodes: "))
num_keys = int(input("Enter the number of keys to insert: "))
replicas = int(input("Enter the number of replicas per node: "))

simulate_load_distribution(num_nodes, num_keys, replicas)
