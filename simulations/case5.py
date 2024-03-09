"""
########################################################
Simulation Case 5: Effect of Key Access Patterns
########################################################

Objective: To evaluate system performance under different key access patterns.

Parameters to Input:
    * Cache capacity
    * Number of keys
    * Access pattern (e.g., uniform, Zipfian, sequential)

Expected Output:
    * A line graph comparing cache hit rate across different access patterns.
    * A line graph comparing average access time across different access patterns.
"""
import sys
sys.path.append('.')
import numpy as np
import matplotlib.pyplot as plt
import time
from lru_cache import LRUCache

def generate_access_pattern(pattern_type, num_keys, num_accesses):
    if pattern_type == "uniform":
        return np.random.randint(0, num_keys, size=num_accesses)
    elif pattern_type == "sequential":
        return np.arange(num_accesses) % num_keys
    elif pattern_type == "zipfian":
        return np.random.zipf(1.2, num_accesses) % num_keys
    else:
        raise ValueError("Unknown pattern type")

def simulate_access_pattern(cache_capacity, num_keys, access_pattern):
    cache = LRUCache(cache_capacity)
    hits = 0
    start_time = time.time()
    
    for key in access_pattern:
        if cache.get(key) != -1:
            hits += 1
        else:
            cache.put(key, f"value_{key}")
    
    total_time = time.time() - start_time
    hit_rate = hits / len(access_pattern)
    avg_access_time = total_time / len(access_pattern)
    
    return hit_rate, avg_access_time

def simulate_key_access_patterns(cache_capacity, num_keys, num_accesses):
    patterns = ["uniform", "sequential", "zipfian"]
    hit_rates = []
    access_times = []

    for pattern in patterns:
        access_pattern = generate_access_pattern(pattern, num_keys, num_accesses)
        hit_rate, avg_access_time = simulate_access_pattern(cache_capacity, num_keys, access_pattern)
        hit_rates.append(hit_rate)
        access_times.append(avg_access_time)

    # Plotting
    x = np.arange(len(patterns))
    width = 0.35

    fig, ax1 = plt.subplots()
    rects1 = ax1.bar(x - width/2, hit_rates, width, label='Hit Rate')

    ax2 = ax1.twinx()
    rects2 = ax2.bar(x + width/2, access_times, width, label='Avg. Access Time', color='orange')

    ax1.set_xlabel('Access Pattern')
    ax1.set_ylabel('Hit Rate', color='blue')
    ax2.set_ylabel('Average Access Time (seconds)', color='orange')
    ax1.set_title('Cache Performance by Access Pattern')
    ax1.set_xticks(x)
    ax1.set_xticklabels(patterns)
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    fig.tight_layout()
    plt.show()

# Input parameters
cache_capacity = int(input("Enter cache capacity: "))
num_keys = int(input("Enter the number of unique keys: "))
num_accesses = int(input("Enter the number of key accesses: "))

simulate_key_access_patterns(cache_capacity, num_keys, num_accesses)
