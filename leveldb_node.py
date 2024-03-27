import plyvel
import os
import logging
import time
from tabulate import tabulate  # You may need to install this package using pip


class LevelDBNode:
    def __init__(self, db_path):
        self.db_path = db_path
        self.db = None
        try:
            if not os.path.exists(db_path):
                os.makedirs(db_path)
            self.db = plyvel.DB(db_path, create_if_missing=True)
        except Exception as e:
            logging.error(f"Error opening LevelDB at {db_path}: {e}")
            if self.db:
                self.db.close()

    def get(self, key):
        key = key.encode('utf-8')
        value = self.db.get(key)
        return value.decode('utf-8') if value else None

    def put(self, key, value):
        try:
            self.db.put(key.encode('utf-8'), value.encode('utf-8'))
            logging.info(f"Key {key} added/updated in LevelDBNode at {self.db_path}")
        except Exception as e:
            logging.error(f"Error adding/updating key {key} in LevelDBNode at {self.db_path}: {e}")

    def write_batch(self, updates):
        with self.db.write_batch() as batch:
            for key, value in updates:
                if value is None:
                    batch.delete(key.encode('utf-8'))
                else:
                    batch.put(key.encode('utf-8'), value.encode('utf-8'))

    def close(self):
        if self.db:
            self.db.close()
            logging.info(f"Closed LevelDB at {self.db_path}")

    def begin_transaction(self):
        return self.db.write_batch(transaction=True)

    def commit_transaction(self, batch):
        batch.write()

    def get_all(self):
        """Simulate fetching all key-value pairs from this node's LevelDB instance."""
        try:
            return [(k.decode('utf-8'), v.decode('utf-8')) for k, v in self.db.iterator()]
        except Exception as e:
            logging.error(f"Error fetching all key-value pairs from LevelDBNode at {self.db_path}: {e}")
            return []