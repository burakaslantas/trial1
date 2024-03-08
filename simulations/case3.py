"""
############################################
Cache Eviction Policy
############################################

Objective: To verify that the LRU cache evicts the least recently used items when it reaches capacity.

Procedure:
    1- Initialize the cache with a known capacity (e.g., 100 items).
    2- Insert items into the cache until it exceeds capacity.
    3- Access a subset of items to mark them as recently used.
    4- Insert additional items to trigger eviction.


Expected Outcome:
    * The items not recently accessed should be evicted from the cache.
    * The cache size should not exceed its maximum capacity after the insertion of new items.
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

# Assuming a function to get the current size of the cache; simulate with random inserts
cache_sizes = []

for i in range(120):  # Exceed the cache capacity
    coordinator.put(f'key{i}', f'value{i}')
    cache_sizes.append(len(coordinator.cache.cache))  # Track cache size

# Plot cache size over time
plt.figure(figsize=(10, 4))
plt.plot(cache_sizes, label='Cache Size')
plt.axhline(y=100, color='r', linestyle='--', label='Capacity')
plt.title('Cache Size Over Time')
plt.xlabel('Operation')
plt.ylabel('Cache Size')
plt.legend()
plt.show()
