"""
############################################
Cache Hit Efficiency
############################################

Objective: To demonstrate the efficiency of the cache by repeatedly accessing a small subset of keys.

Procedure:
    1- Pre-populate the LevelDB nodes with a large dataset (e.g., 10,000 key-value pairs).
    2- Populate the cache with a subset of keys (e.g., the first 100 keys).
    3- Repeatedly access these keys in a loop to ensure they are served from the cache.

Expected Outcome:
    * The cache hit rate should be high, close to 100% for these keys.
    * Response times for these get operations should be significantly lower than those for keys not in the cache.
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

hits, misses = 0, 0

# Function to simulate cache hits and misses
def simulate_cache_hits_misses(key_range, accesses):
    global hits, misses
    for _ in range(accesses):
        key = f'key{np.random.randint(0, key_range)}'
        if coordinator.get(key) is not None:
            hits += 1
        else:
            misses += 1

# Populate cache with a subset of keys
for i in range(10000):
    coordinator.put(f'key{i}', f'value{i}')

simulate_cache_hits_misses(10000, 10000)

# Log and plot results
logger.info(f"Cache Hits: {hits}, Cache Misses: {misses}")
plt.figure(figsize=(5, 3))
plt.bar(['Hits', 'Misses'], [hits, misses], color=['green', 'red'])
plt.title('Cache Hits vs Misses')
plt.ylabel('Count')
plt.show()
