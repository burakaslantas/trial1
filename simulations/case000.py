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
        for node_url, key_values in all_key_values.items():
            node_counters[node_url] = len(key_values)
            for key, value in key_values.items():  # assuming key_values is a dict
                data.append({"Node": node_url, "Key": key, "Value": value})

        # Clear the console screen
        print("\033[H\033[J", end="")
        print(tabulate(data, headers="keys", tablefmt="grid"))

        # Display the count of key-value pairs for each node
        counters_data = [{"Node": node, "Count": count} for node, count in node_counters.items()]
        print("\nNode Key-Value Pair Counts:")
        print(tabulate(counters_data, headers="keys", tablefmt="grid"))

        time.sleep(5)  # Refresh every 5 seconds

if __name__ == "__main__":
    node_urls = ['http://192.168.1.110:5000', 'http://192.168.1.113:5000', 'http://192.168.1.119:5000']  # URLs of the node REST APIs
    coordinator = Coordinator(node_urls=node_urls, cache_capacity=10, replicas=50)

    # Fill in some data for demonstration purposes
    for i in range(100):
        coordinator.put("key" + str(i), "value" + str(i))
    
    # Fetch and print the data for demonstration purposes
    # for i in range(5):
    #    print(coordinator.get("key" + str(i)))

    # Display the data in a tabulated format
    display_nodes_data(coordinator)
