import sys
sys.path.append('.')
import matplotlib.pyplot as plt
from consistent_hashing import ConsistentHashing

# Parameters
node_count = 5
key_count = 10000

# Step 1: Setup Phase
nodes = [f'node_{i}' for i in range(node_count)]
hashing = ConsistentHashing(nodes)

# Step 2: Action Phase - Distribute keys across nodes using consistent hashing
node_key_distribution = {node: 0 for node in nodes}
for key in range(key_count):
    node = hashing.get_node(str(key))
    node_key_distribution[node] += 1

# Step 3: Measurement Phase - Already done in action phase

# Step 4: Output Phase - Generate histogram
plt.figure(figsize=(10, 6))
plt.bar(node_key_distribution.keys(), node_key_distribution.values(), color='skyblue')
plt.title("Key Distribution Across Nodes")
plt.xlabel("Nodes")
plt.ylabel("Number of Keys")
plt.grid(axis='y', linestyle='--', linewidth=0.7)
plt.show()
