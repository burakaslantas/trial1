"""
############################################
Scalability Test
############################################

Objective: To evaluate how the system scales with an increasing number of get and put operations.

Procedure:
    1- Start with a baseline number of operations per second (e.g., 100 ops/sec).
    2- Gradually increase the load on the system (e.g., up to 1,000 ops/sec).
    3- Monitor the system's response time, throughput, and cache hit rate.

Expected Outcome:
    * The system should handle the increased load up to a certain point without significant degradation in performance.
    * Beyond a certain load threshold, you may observe increased response times or decreased throughput,
    indicating the system's scalability limits under the current configuration.
"""
import sys
import time
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

ops_range = range(100, 1100, 200)  # Define different loads
response_times = []

for ops in ops_range:
    start_time = time.time()
    for i in range(ops):
        coordinator.put(f'scale_key{i}', f'scale_value{i}')
    elapsed_time = time.time() - start_time
    response_times.append(elapsed_time / ops)  # Calculate average response time per operation

# Plot the results
plt.figure(figsize=(10, 5))
plt.plot(ops_range, response_times, marker='o', linestyle='-', color='b')
plt.title('Response Time Scalability Test')
plt.xlabel('Number of Operations')
plt.ylabel('Average Response Time per Operation (seconds)')
plt.grid(True)
plt.show()
