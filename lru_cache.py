class ListNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {} # key -> node
        # Initialize the head and tail with dummy nodes to avoid empty state checks
        self.head = ListNode(0, 0)
        self.tail = ListNode(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def _add(self, node):
        # Add the new node right after the head
        nxt = self.head.next
        self.head.next = node
        node.prev = self.head
        node.next = nxt
        nxt.prev = node

    def _remove(self, node):
        # Remove the given node from the list
        prev = node.prev
        nxt = node.next
        prev.next = nxt
        nxt.prev = prev

    def get(self, key: int) -> int:
        if key in self.cache:
            node = self.cache[key]
            self._remove(node) # Remove from current position
            self._add(node) # Add to the front (most recently used)
            return node.value
        return -1
    
    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self._remove(self.cache[key]) # Update existing node
        elif len(self.cache) >= self.capacity:
            # Evict least recently used node
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]
        new_node = ListNode(key, value)
        self.cache[key] = new_node
        self._add(new_node)
