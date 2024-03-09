import hashlib
import bisect

class ConsistentHashing:
    def __init__(self, nodes=None, replicas=100):
        self.nodes = set()
        self.replicas = replicas
        self.ring = []
        self._sorted_keys = []
        if nodes:
            for node in nodes:
                self.add_node(node)

    def _hash(self, key):
        return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16)

    def add_node(self, node):
        for i in range(self.replicas):
            virtual_node = f'{node}-{i}'
            key = self._hash(virtual_node)
            bisect.insort(self._sorted_keys, key)
            self.ring.append((key, node))
        self.nodes.add(node)

    def remove_node(self, node):
        for i in range(self.replicas):
            virtual_node = f'{node}-{i}'
            key = self._hash(virtual_node)
            self._sorted_keys.remove(key)
            self.ring.remove((key, node))
        self.nodes.discard(node)

    def get_node(self, key):
        if not self.ring:
            return None
        key_hash = self._hash(key)
        index = bisect.bisect(self._sorted_keys, key_hash) % len(self.ring)
        return self.ring[index][1]
