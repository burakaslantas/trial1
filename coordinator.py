from lru_cache import LRUCache
from leveldb_node import LevelDBNode

class Coordinator:
    def __init__(self, node_paths, cache_capacity=100):
        self.nodes = [LevelDBNode(path) for path in node_paths] # Initialize LevelDB nodes based on provided paths
        self.cache = LRUCache(cache_capacity) # Initialize the LRU cache with the specified capacity
        self.current_node = 0 # Counter to keep track of the current node for round-robin strategy

    def get(self, key):
        # Attempt to retrieve the value from cache first
        value = self.cache.get(key)
        if value is not None:
            return value  # Cache hit, return the value immediately
        
        # Cache miss, attempt to retrieve the value from the current LevelDB node
        value = self.nodes[self.current_node].get(key)
        if value:
            # If the value is found, update the cache before returning the value
            self.cache.put(key, value)
        return value

    def put(self, key, value):
        self.cache.put(key, value) # Update the cache with the new value
        self.nodes[self.current_node].put(key, value) # Store the value in the current LevelDB node
        self.current_node = (self.current_node + 1) % len(self.nodes) # Move to the next node in a round-robin fashion

    def close_all(self):
        # Ensure all LevelDB node connections are properly closed
        for node in self.nodes:
            node.close()
