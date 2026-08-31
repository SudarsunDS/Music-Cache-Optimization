from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Node:
    key: Optional[int] = None
    value: Any = None
    prev: Optional["Node"] = None
    next: Optional["Node"] = None


class LRUCache:
    """
    O(1) LRU Cache implementation using:
    - HashMap (Python Dictionary)
    - Doubly Linked List
    """

    def __init__(self, capacity: int = 100):

        if capacity <= 0:
            raise ValueError("Capacity must be greater than 0")

        self.capacity = capacity
        self.cache = {}

        # Dummy nodes simplify insertion and deletion
        self.head = Node()
        self.tail = Node()

        self.head.next = self.tail
        self.tail.prev = self.head

        # Performance metrics
        self.hits = 0
        self.misses = 0
        self.evictions = 0

    def _remove(self, node):
        """Remove a node from the doubly linked list."""

        previous = node.prev
        next_node = node.next

        previous.next = next_node
        next_node.prev = previous

    def _insert_after_head(self, node):
        """Insert node as the Most Recently Used item."""

        node.prev = self.head
        node.next = self.head.next

        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        """Retrieve a value and mark it as recently used."""

        node = self.cache.get(key)

        if node is None:
            self.misses += 1
            return None

        self.hits += 1

        # Move accessed node to MRU position
        self._remove(node)
        self._insert_after_head(node)

        return node.value

    def put(self, key, value):
        """Insert or update a value in the cache."""

        # Update existing key
        if key in self.cache:

            node = self.cache[key]
            node.value = value

            self._remove(node)
            self._insert_after_head(node)

            return

        # Insert new node
        new_node = Node(key, value)

        self.cache[key] = new_node
        self._insert_after_head(new_node)

        # Evict LRU item if capacity exceeded
        if len(self.cache) > self.capacity:

            lru_node = self.tail.prev

            self._remove(lru_node)

            del self.cache[lru_node.key]

            self.evictions += 1

    def clear(self):
        """Clear all cached items and reset metrics."""

        self.cache.clear()

        self.head.next = self.tail
        self.tail.prev = self.head

        self.hits = 0
        self.misses = 0
        self.evictions = 0

    def stats(self):
        """Return cache performance metrics."""

        total_requests = self.hits + self.misses

        hit_rate = (
            (self.hits / total_requests) * 100
            if total_requests > 0
            else 0
        )

        return {
            "capacity": self.capacity,
            "size": len(self.cache),
            "hits": self.hits,
            "misses": self.misses,
            "evictions": self.evictions,
            "total_requests": total_requests,
            "hit_rate_percent": round(hit_rate, 2)
        }

    def keys_mru_to_lru(self):
        """Return cached keys from MRU to LRU."""

        keys = []

        current = self.head.next

        while current != self.tail:

            keys.append(current.key)

            current = current.next

        return keys
