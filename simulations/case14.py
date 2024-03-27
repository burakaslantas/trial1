import sys
sys.path.append('.')
import matplotlib.pyplot as plt
import random
import time
from coordinator import Coordinator

# Parameters
node_paths = ['node1', 'node2', 'node3', 'node4']
total_keys = 1000
cache_sizes = [10, 50, 100, 500, 1000]
operation_count = 1000
read_write_ratio = 0.8  # 80% reads, 20% writes

# Function to perform mixed workload
def perform_workload(coordinator, operations):
    start_time = time.time()
    read_operations = 0
    write_operations = 0

    for _ in range(operations):
        key = str(random.randint(0, total_keys - 1))
        if random.random() < read_write_ratio:
            coordinator.get(key)
            read_operations += 1
        else:
            coordinator.put(key, f"value-{key}")
            write_operations += 1

    end_time = time.time()
    elapsed_time = end_time - start_time
    return elapsed_time, read_operations, write_operations

# Pre-populate the database
base_coordinator = Coordinator(node_paths, cache_capacity=1000, replicas=100, replication_factor=2)
for key in range(total_keys):
    base_coordinator.put(str(key), f"value-{key}")

# Measurement Phase
latencies = []
throughputs = []

for cache_size in cache_sizes:
    coordinator = Coordinator(node_paths, cache_capacity=cache_size, replicas=100, replication_factor=2)
    elapsed_time, read_ops, write_ops = perform_workload(coordinator, operation_count)
    latencies.append(elapsed_time)
    throughput = (read_ops + write_ops) / elapsed_time
    throughputs.append(throughput)

# Output Phase
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.plot(cache_sizes, latencies, marker='o', linestyle='-')
plt.title("Average Latency vs. Cache Size")
plt.xlabel("Cache Size")
plt.ylabel("Average Latency (seconds)")
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(cache_sizes, throughputs, marker='o', linestyle='-', color='green')
plt.title("Throughput vs. Cache Size")
plt.xlabel("Cache Size")
plt.ylabel("Throughput (operations/second)")
plt.grid(True)

plt.tight_layout()
plt.show()
