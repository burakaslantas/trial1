"""
########################################################
Simulation Case 3: Resilience to Node Failures
########################################################

Objective: To simulate the system's resilience by removing nodes and observing the effect on key availability and load distribution.

Parameters to Input:
    * Number of initial nodes
    * Number of keys to insert
    * Sequence of node removals

Expected Output:
    * A line graph showing the number of keys accessible versus the number of nodes removed.
    * A histogram showing the load distribution among remaining nodes after each removal.
"""
import sys
sys.path.append('.')
import matplotlib.pyplot as plt
from consistent_hashing import ConsistentHashing
import numpy as np

def simulate_node_failures(num_nodes, num_keys, num_failures):
    hashing = ConsistentHashing(replicas=100)
    nodes = [f'node_{i}' for i in range(num_nodes)]
    for node in nodes:
        hashing.add_node(node)
    
    # Simulate inserting keys
    keys = [f'key_{i}' for i in range(num_keys)]
    initial_distribution = {node: 0 for node in nodes}
    for key in keys:
        node = hashing.get_node(key)
        initial_distribution[node] += 1

    accessible_keys = []
    load_distributions = []

    for i in range(num_failures + 1):
        # Calculate accessible keys after failures
        current_accessible_keys = 0
        current_distribution = {node: 0 for node in nodes if node in hashing.nodes}
        for key in keys:
            node = hashing.get_node(key)
            if node:  # Node might be None if all nodes are removed
                current_accessible_keys += 1
                current_distribution[node] += 1

        accessible_keys.append(current_accessible_keys)
        load_distributions.append(current_distribution)

        if i < num_failures:
            # Remove a node
            hashing.remove_node(nodes[i])

    # Plotting
    plt.figure(figsize=(14, 6))

    # Plot accessible keys over failures
    plt.subplot(1, 2, 1)
    plt.plot(range(num_failures + 1), accessible_keys, marker='o')
    plt.xlabel('Number of Node Failures')
    plt.ylabel('Number of Accessible Keys')
    plt.title('Accessible Keys vs. Node Failures')

    # Plot load distribution after all failures
    plt.subplot(1, 2, 2)
    final_distribution = load_distributions[-1]
    plt.bar(final_distribution.keys(), final_distribution.values(), color='skyblue')
    plt.xlabel('Node')
    plt.ylabel('Number of Keys')
    plt.title('Load Distribution After All Failures')
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

# Input parameters
num_nodes = int(input("Enter the number of initial nodes: "))
num_keys = int(input("Enter the number of keys to insert: "))
num_failures = int(input("Enter the number of nodes to fail: "))

simulate_node_failures(num_nodes, num_keys, num_failures)
