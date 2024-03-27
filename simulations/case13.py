import sys
sys.path.append('.')
import matplotlib.pyplot as plt
import random
import time
from threading import Thread
from coordinator import Coordinator

# Parameters
node_paths = ['node1', 'node2', 'node3', 'node4']
total_keys = 500
health_check_interval = 5  # seconds

# Initialize Coordinator
coordinator = Coordinator(node_paths=node_paths, cache_capacity=100, replicas=100, replication_factor=2)

# Populate the system
for key in range(total_keys):
    coordinator.put(str(key), f"value-{key}")

def simulate_node_failure(node_path, fail_duration=10):
    """Simulates node failure by removing it and then adding it back after some time."""
    coordinator.remove_node(node_path)
    time.sleep(fail_duration)
    coordinator.add_node(node_path)

def health_check_loop():
    while True:
        coordinator.check_node_health()
        time.sleep(health_check_interval)

# Start the health check in a separate thread
health_check_thread = Thread(target=health_check_loop)
health_check_thread.start()

# Simulate node failures in separate threads
for node in node_paths[1:3]:  # Simulate failure for 2 nodes
    Thread(target=simulate_node_failure, args=(node, 15)).start()

# Track system status
times = []
healthy_nodes_counts = []
request_success_rates = []

start_time = time.time()
while time.time() - start_time < 60:  # Run simulation for 1 minute
    times.append(time.time() - start_time)
    healthy_nodes_counts.append(len(coordinator.nodes))
    successful_requests = sum(coordinator.get(str(key)) is not None for key in range(total_keys))
    request_success_rates.append(successful_requests / total_keys)
    time.sleep(2)

# Plotting
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.plot(times, healthy_nodes_counts, label='Healthy Nodes')
plt.title("Number of Healthy Nodes Over Time")
plt.xlabel("Time (seconds)")
plt.ylabel("Number of Healthy Nodes")
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(times, request_success_rates, label='Request Success Rate', color='green')
plt.title("Request Success Rate Over Time")
plt.xlabel("Time (seconds)")
plt.ylabel("Success Rate")
plt.legend()

plt.tight_layout()
plt.show()
