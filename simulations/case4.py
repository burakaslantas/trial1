"""
############################################
Recovery from Node Failure
############################################

Objective: To simulate node failure and verify that the system can handle such failures gracefully, 
assuming a manual failover or replication mechanism is in place.

Procedure:
    1- Pre-populate all LevelDB nodes with data.
    2- Simulate a node failure by disabling one of the nodes.
    3- Attempt to perform get and put operations through the coordinator.
    4- Manually redistribute the data from the failed node to the remaining nodes (simulated).

Expected Outcome:
    * The system should continue to operate, albeit with possible temporary degradation.
    * Once data is redistributed, the system should return to normal operation.
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

# Manually disable a node for simulation purposes
def disable_node(node_index):
    if 0 <= node_index < len(coordinator.nodes):
        coordinator.nodes[node_index] = None  # Simulate node failure by setting it to None
        logger.info(f"Node {node_index} has been simulated as failed.")

disable_node(1)  # Simulate failure of the second node

# Attempt to perform operations
try:
    coordinator.put('key_failure_test', 'value_test')
    value = coordinator.get('key_failure_test')
    logger.info(f"Operation successful. Retrieved value: {value}")
except Exception as e:
    logger.info(f"Operation failed due to node failure: {e}")

# Note: Real implementation should handle rerouting or disabling operations to the failed node.
