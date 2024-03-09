"""
########################################################
Simulation Case 4: Replication Impact on Load Balancing
########################################################
Objective: To observe how the number of replicas affects the load balancing across the nodes.

Parameters to Input:
    * Number of nodes
    * Number of keys to insert
    * Range of replica counts to test

Expected Output:
    * A line graph showing the standard deviation of key distribution across nodes for different numbers of replicas. 
    A lower standard deviation indicates better load balancing.
"""

import sys
sys.path.append('.')
import matplotlib.pyplot as plt
from consistent_hashing import ConsistentHashing
import numpy as np

def simulate_replication_impact(num_nodes, num_keys, replica_range):
    variances = []

    for replicas in replica_range:
        hashing = ConsistentHashing(replicas=replicas)
        for i in range(num_nodes):
            node_name = f'node_{i}'
            hashing.add_node(node_name)

        node_distribution = {f'node_{i}': 0 for i in range(num_nodes)}
        for i in range(num_keys):
            key = f'key_{i}'
            node = hashing.get_node(key)
            node_distribution[node] += 1

        # Calculate variance
        values = np.array(list(node_distribution.values()))
        variance = np.var(values)
        variances.append(variance)

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(replica_range, variances, marker='o', linestyle='-', color='b')
    plt.xlabel('Number of Replicas')
    plt.ylabel('Variance in Key Distribution')
    plt.title('Replication Impact on Load Balancing')
    plt.grid(True)
    plt.show()

# Input parameters
num_nodes = int(input("Enter the number of nodes: "))
num_keys = int(input("Enter the number of keys to insert: "))
start_replicas = int(input("Enter the start number of replicas: "))
end_replicas = int(input("Enter the end number of replicas: "))

replica_range = range(start_replicas, end_replicas + 1)

simulate_replication_impact(num_nodes, num_keys, replica_range)
