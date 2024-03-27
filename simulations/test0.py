import sys
sys.path.append('.')
import unittest
import tempfile
import shutil
from coordinator import Coordinator

class TestSystem(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for each LevelDB instance
        self.node_paths = [tempfile.mkdtemp() for _ in range(3)]
        self.coordinator = Coordinator(self.node_paths, cache_capacity=10, replicas=3, replication_factor=2)

    def test_put_and_get(self):
        key, value = 'test_key', 'test_value'
        self.coordinator.put(key, value)
        retrieved_value = self.coordinator.get(key)
        self.assertEqual(retrieved_value, value, "Value retrieved does not match the expected value.")

    def test_replication(self):
        key, value = 'test_key', 'test_value'
        self.coordinator.put(key, value)

        # Fetch the primary node for the key and get the value
        primary_node = self.coordinator.get_node(key)
        primary_value = primary_node.get(key)
        self.assertEqual(primary_value, value, "Primary node value mismatch.")

        # Fetch the node that should hold the replica and get the value
        # We convert the db_path to the corresponding hash to find the replica index
        primary_node_hash = self.coordinator.hashing._hash(primary_node.db_path)
        primary_index = self.coordinator.hashing.find_node_index(primary_node_hash)
        previous_index = (primary_index - 1) % len(self.coordinator.hashing.ring)
        previous_node_path = self.coordinator.hashing.ring[previous_index][1]
        previous_node = self.coordinator.nodes[previous_node_path]
        replica_value = previous_node.get(key)
        self.assertEqual(replica_value, value, "Replica node value mismatch.")


    def tearDown(self):
        # Close all LevelDB connections and delete temporary directories
        self.coordinator.close_all()
        for path in self.node_paths:
            shutil.rmtree(path)

if __name__ == '__main__':
    unittest.main()
