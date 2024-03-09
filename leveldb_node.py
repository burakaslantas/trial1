# leveldb_node.py
import plyvel
import os

class LevelDBNode:
    def __init__ (self, db_path):
        # Ensure directory exists
        if not os.path.exists(db_path):
            os.makedirs(db_path)
        self.db = plyvel.DB(db_path, create_if_missing=True)
    
    def get(self, key):
        # Plyvel fetches bytes, so it's important to encode the key and decode the value
        key = key.encode('utf-8')
        value = self.db.get(key)
        return value.decode('utf-8') if value else None
    
    def put(self, key, value):
        # Both key and value are stored as bytes in LevelDB
        self.db.put(key.encode('utf-8'), value.encode('utf-8'))

    """
    def list_all(self):
        return {key.decode('utf-8'): value.decode('utf-8') for key, value in self.db.iterator()}
    """
    
    def close(self):
        self.db.close()
