# coordinator.py
from lru_cache import LRUCache
from leveldb_node import LevelDBNode
from consistent_hashing import ConsistentHashing  # Assuming you have a ConsistentHashing class implemented

class Coordinator:
    def __init__(self, node_paths, cache_capacity=100, replicas=100):
        self.cache = LRUCache(cache_capacity)  # Initialize the LRU cache with the specified capacity
        self.nodes = {}  # This will store the node instances keyed by their paths
        self.hashing = ConsistentHashing(replicas=replicas)  # Initialize consistent hashing
        
        # Initialize LevelDB nodes and add them to the consistent hashing ring
        for path in node_paths:
            node = LevelDBNode(path)
            self.nodes[path] = node
            self.hashing.add_node(path)

    def get_node(self, key):
        # Use consistent hashing to find the node for a given key
        node_path = self.hashing.get_node(key)
        return self.nodes[node_path]

    def get(self, key):
        # Attempt to retrieve the value from cache first
        value = self.cache.get(key)
        if value is not None:
            return value  # Cache hit
        
        # Cache miss, retrieve the value from the appropriate LevelDB node using consistent hashing
        node = self.get_node(key)
        value = node.get(key)
        if value:
            # If the value is found, update the cache before returning the value
            self.cache.put(key, value)
        return value

    def put(self, key, value):
        # Update the cache with the new value
        self.cache.put(key, value)
        
        # Store the value in the appropriate LevelDB node using consistent hashing
        node = self.get_node(key)
        node.put(key, value)

    def close_all(self):
        # Ensure all LevelDB node connections are properly closed
        for node in self.nodes.values():
            node.close()
