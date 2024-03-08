import sys
sys.path.append('.')
from coordinator import Coordinator

node_paths = ['./db_node1', './db_node2', './db_node3'] # Define paths for each simulated node's LevelDB instance
coordinator = Coordinator(node_paths, cache_capacity=100) # Initialize the coordinator with the paths and a cache capacity

# Example operations
coordinator.put("key1", "value1")
print("Retrieved:", coordinator.get("key1"))

coordinator.close_all()