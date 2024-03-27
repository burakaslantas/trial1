# coordinator.py

import logging
import requests  # You need to install this package if not already installed
from lru_cache import LRUCache
from consistent_hashing import ConsistentHashing

logging.basicConfig(level=logging.INFO)

class Coordinator:
    def __init__(self, node_urls, cache_capacity=100, replicas=100):
        self.cache = LRUCache(cache_capacity)
        self.nodes = {}  # This will store the URL of each node
        self.hashing = ConsistentHashing(replicas=replicas)

        for url in node_urls:
            self.nodes[url] = url  # Store the URL for network access
            self.hashing.add_node(url)

    def get_node(self, key):
        node_url = self.hashing.get_node(key)
        return self.nodes[node_url]

    def get(self, key):
        value = self.cache.get(key)
        if value is not None:
            return value

        node_url = self.get_node(key)
        try:
            response = requests.get(f"{node_url}/get/{key}")
            if response.status_code == 200:
                value = response.json()['value']
                self.cache.put(key, value)
                return value
            else:
                logging.error(f"Error fetching key {key} from {node_url}")
        except Exception as e:
            logging.error(f"Network error when accessing {node_url}: {e}")
        return None

    def put(self, key, value):
        node_url = self.get_node(key)
        try:
            response = requests.post(f"{node_url}/put", json={'key': key, 'value': value})
            if response.status_code == 200:
                self.cache.put(key, value)
            else:
                logging.error(f"Error putting key {key} to {node_url}")
        except Exception as e:
            logging.error(f"Network error when accessing {node_url}: {e}")

    def get_all_key_values(self):
        all_data = {}
        for url in self.nodes.values():
            try:
                response = requests.get(f"{url}/all")
                if response.status_code == 200:
                    all_data[url] = response.json()
                else:
                    logging.error(f"Error fetching all data from {url}")
            except Exception as e:
                logging.error(f"Network error when accessing {url}: {e}")
        return all_data
    
    def get_key_distribution(self):
        distribution = {}
        for url in self.nodes.values():
            try:
                response = requests.get(f"{url}/key-count")
                if response.status_code == 200:
                    node_data = response.json()
                    distribution[url] = node_data.get('key_count', 0)
                else:
                    logging.error(f"Error fetching key count from {url}")
                    distribution[url] = 0
            except Exception as e:
                logging.error(f"Network error when accessing {url}: {e}")
                distribution[url] = 0
        return distribution
    
    def check_health(self):
        health_status = {}
        for node_url in self.nodes.values():
            try:
                response = requests.get(f"{node_url}/stats")  # Assuming /stats also gives a basic health indication
                health_status[node_url] = 'Up' if response.status_code == 200 else 'Down'
            except Exception as e:
                logging.error(f"Error checking health for {node_url}: {e}")
                health_status[node_url] = 'Error'
        return health_status
    
    def aggregate_stats(self):
        total_keys = 0
        total_size = 0
        for node_url in self.nodes.values():
            try:
                response = requests.get(f"{node_url}/stats")
                if response.status_code == 200:
                    node_stats = response.json()
                    total_keys += node_stats.get('key_count', 0)
                    total_size += node_stats.get('db_size', 0)
            except Exception as e:
                logging.error(f"Error aggregating stats from {node_url}: {e}")
        return {'total_keys': total_keys, 'total_size': total_size}




# Example usage
# node_urls = ['http://machine1:5000', 'http://machine2:5000']  # URLs of the node REST APIs
# coordinator = Coordinator(node_urls)
