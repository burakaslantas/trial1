import sys
sys.path.append('.')
import time
import random
import matplotlib.pyplot as plt
from leveldb_node import LevelDBNode
from lru_cache import LRUCache

# Parameters
total_keys = 10000
operation_count = 1000
cache_capacity = 500  # Adjust based on your needs

# Initialize LevelDB and Cache
leveldb_node = LevelDBNode('./case10_db')
cache = LRUCache(cache_capacity)

# Step 1: Setup Phase - Populate the database
for key in range(total_keys):
    leveldb_node.put(str(key), f"value-{key}")

# Function to perform read operations
def perform_reads(use_cache):
    latencies = []
    for _ in range(operation_count):
        key = str(random.randint(0, total_keys - 1))
        
        start_time = time.time()
        
        if use_cache:
            # First try to get from cache
            value = cache.get(key)
            if value is None:
                # Cache miss, get from LevelDB and put it in cache
                value = leveldb_node.get(key)
                cache.put(key, value)
        else:
            # Directly get from LevelDB
            value = leveldb_node.get(key)
        
        end_time = time.time()
        latencies.append(end_time - start_time)
    
    return latencies

# Step 2 & 3: Action and Measurement Phase
latencies_with_cache = perform_reads(use_cache=True)
latencies_without_cache = perform_reads(use_cache=False)

# Step 4: Output Phase - Generate graph
plt.figure(figsize=(10, 6))
plt.plot(latencies_with_cache, label='With Cache')
plt.plot(latencies_without_cache, label='Without Cache')
plt.title("Read Latency Comparison")
plt.xlabel("Operation Count")
plt.ylabel("Latency (seconds)")
plt.legend()
plt.grid(True)
plt.show()
