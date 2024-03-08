"""
############################################
Load Distribution Among Nodes
############################################

Objective: To test the round-robin distribution mechanism's effectiveness in evenly distributing the write load across all LevelDB nodes.

Procedure:
    1- Perform a sequence of put operations (e.g., 1,000 operations) on the coordinator.
    2- Record the distribution of keys across the LevelDB nodes.

Expected Outcome:
    * Each node should have a roughly equal number of new keys, demonstrating effective load distribution.
"""

import sys
sys.path.append('.')
import matplotlib.pyplot as plt
import numpy as np
from coordinator import Coordinator
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()

# Initialize the coordinator (update paths as needed)
node_paths = ['./db_node1', './db_node2', './db_node3']
coordinator = Coordinator(node_paths, cache_capacity=100)

key_counts = [0] * len(node_paths)  # Initialize key counts per node

for i in range(1000):
    key = f'key{i}'
    coordinator.put(key, f'value{i}')
    key_counts[coordinator.current_node] += 1

# Log and plot the distribution of keys across nodes
logger.info(f"Key distribution across nodes: {key_counts}")
plt.figure(figsize=(5, 3))
plt.bar(range(len(node_paths)), key_counts, tick_label=[f'Node {i+1}' for i in range(len(node_paths))])
plt.title('Key Distribution Across Nodes')
plt.xlabel('Node')
plt.ylabel('Number of Keys')
plt.show()
