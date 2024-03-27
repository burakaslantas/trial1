import hashlib
import bisect

class ConsistentHashing:
    """
    Implements consistent hashing to distribute keys across a set of nodes,
    minimizing redistribution when nodes change. Each node has multiple replicas
    in the hash space to distribute the load evenly.
    """

    def __init__(self, nodes=None, replicas=100):
        """
        Initializes the consistent hashing ring.

        Args:
            nodes (list of str): An initial list of nodes to add to the hash ring.
            replicas (int): The number of virtual nodes (replicas) for each real node.
        """
        self.nodes = set()
        self.replicas = replicas
        self.ring = dict()
        self.sorted_keys = []
        if nodes:
            for node in nodes:
                self.add_node(node)

    def _hash(self, key):
        """
        Generates a consistent hash value for the given key.

        Args:
            key (str): The key to hash.

        Returns:
            int: A consistent hash value of the key.
        """
        return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16)

    def add_node(self, node):
        """
        Adds a node and its replicas to the hash ring.

        Args:
            node (str): The node to add.
        """
        for i in range(self.replicas):
            virtual_node_key = f'{node}-{i}'
            hash_value = self._hash(virtual_node_key)
            self.ring[hash_value] = node
            bisect.insort(self.sorted_keys, hash_value)

    def remove_node(self, node):
        """
        Removes a node and its replicas from the hash ring.

        Args:
            node (str): The node to remove.
        """
        self.sorted_keys = [k for k in self.sorted_keys if self.ring[k] != node]
        self.ring = {k: n for k, n in self.ring.items() if n != node}
        self.nodes.discard(node)

    def get_node(self, key):
        """
        Gets the node responsible for the given key.

        Args:
            key (str): The key to find the responsible node for.

        Returns:
            str: The node responsible for the key.
        """
        if not self.sorted_keys:
            return None
        hash_value = self._hash(key)
        index = bisect.bisect_right(self.sorted_keys, hash_value) % len(self.sorted_keys)
        return self.ring[self.sorted_keys[index]]