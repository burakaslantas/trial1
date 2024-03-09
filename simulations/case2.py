"""
########################################################
Simulation Case 2: Cache Performance Impact
########################################################

Objective: To understand how different cache capacities affect hit rates and performance.

Parameters to Input:
    * Cache capacity (number of items)
    * Number of keys accessed
    * Access pattern distribution (e.g., uniform, Zipfian)

Expected Output:
    * A line graph showing cache hit rate versus cache capacity.
    * A line graph showing average access time versus cache capacity.
"""

import sys
sys.path.append('.')
import numpy as np
import matplotlib.pyplot as plt
from lru_cache import LRUCache
import time
import random

def simulate_cache_performance(access_pattern, num_accesses, max_cache_capacity):
    hit_rates = []
    access_times = []
    
    for capacity in range(1, max_cache_capacity + 1):
        cache = LRUCache(capacity)
        hit_count = 0
        total_time = 0
        
        for i in range(num_accesses):
            key = access_pattern[i % len(access_pattern)]
            start_time = time.time()
            if cache.get(key) == -1:
                # Simulate cache miss delay
                time.sleep(0.001)
                cache.put(key, f"value_{key}")
            else:
                hit_count += 1
            total_time += (time.time() - start_time)
        
        hit_rate = hit_count / num_accesses
        avg_access_time = total_time / num_accesses
        hit_rates.append(hit_rate)
        access_times.append(avg_access_time)
    
    # Plotting results
    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('Cache Capacity')
    ax1.set_ylabel('Hit Rate', color=color)
    ax1.plot(range(1, max_cache_capacity + 1), hit_rates, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:blue'
    ax2.set_ylabel('Average Access Time (s)', color=color)  # we already handled the x-label with ax1
    ax2.plot(range(1, max_cache_capacity + 1), access_times, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.title('Cache Performance Impact Analysis')
    plt.show()

# Parameters
max_cache_capacity = int(input("Enter the maximum cache capacity to test: "))
num_accesses = int(input("Enter the number of key accesses: "))
access_pattern_type = input("Enter access pattern (uniform/zipfian): ")

# Generate access pattern
keys = list(range(100))  # Assuming 100 unique keys
if access_pattern_type.lower() == 'zipfian':
    access_pattern = np.random.zipf(1.2, num_accesses)
else:
    access_pattern = random.choices(keys, k=num_accesses)

simulate_cache_performance(access_pattern, num_accesses, max_cache_capacity)
