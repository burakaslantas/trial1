import logging
from lru_cache import LRUCache
from leveldb_node import LevelDBNode
from consistent_hashing import ConsistentHashing

logging.basicConfig(level=logging.INFO)

class Coordinator:
    def __init__(self, node_paths, cache_capacity=100, replicas=100):
        self.cache = LRUCache(cache_capacity)
        self.nodes = {}
        self.hashing = ConsistentHashing(replicas=replicas)

        for path in node_paths:
            node = LevelDBNode(path)
            self.nodes[path] = node
            self.hashing.add_node(path)

    def get_node(self, key):
        node_path = self.hashing.get_node(key)
        return self.nodes[node_path]

    def get(self, key):
        value = self.cache.get(key)
        if value is not None:
            return value

        node = self.get_node(key)
        value = node.get(key)
        if value:
            self.cache.put(key, value)
        return value

    def put(self, key, value):
        node = self.get_node(key)
        node.put(key, value)
        self.cache.put(key, value)

    def close_all(self):
        for node in self.nodes.values():
            node.close()
            logging.info("Closed connection to LevelDB node")
    
    def get_all_key_values(self):
        all_data = {}
        for path, node in self.nodes.items():
            try:
                all_data[path] = node.get_all()
            except Exception as e:
                logging.error(f"Error getting all key-value pairs from {path}: {e}")
        return all_data

