# Assuming the classes are already defined as per your code snippets
import sys
sys.path.append('.')
from coordinator import Coordinator
from tabulate import tabulate
import time

def display_nodes_data(coordinator):
    while True:
        data = []
        node_counters = {}  # To keep track of the number of key-value pairs per node

        all_key_values = coordinator.get_all_key_values()
        for node_path, key_values in all_key_values.items():
            node_counters[node_path] = len(key_values)
            for key, value in key_values:
                data.append({"Node": node_path, "Key": key, "Value": value})

        # Clear the console screen
        print("\033[H\033[J", end="")
        print(tabulate(data, headers="keys", tablefmt="grid"))

        # Display the count of key-value pairs for each node
        counters_data = [{"Node": node, "Count": count} for node, count in node_counters.items()]
        print("\nNode Key-Value Pair Counts:")
        print(tabulate(counters_data, headers="keys", tablefmt="grid"))

        time.sleep(5)  # Refresh every 5 seconds


# Example usage
if __name__ == "__main__":
    node_paths = ["./dbnode1", "./dbnode2", "./dbnode3"]
    coordinator = Coordinator(node_paths=node_paths, cache_capacity=10, replicas=50)

    # Fill in some data for demonstration purposes
    for i in range(1000):
        coordinator.put("key"+str(i), "value"+str(i))

    try:
        display_nodes_data(coordinator)
    finally:
        coordinator.close_all()
