#!/usr/bin/env python3
"""FIFO caching policy"""


from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """FIFOCache class inherits from BaseCaching
    and implements a FIFO caching system"""
    def __init__(self):
        """Initialize the FIFOCache instance."""
        super().__init__()

    def put(self, key, item):
        """Add an item to the cache with FIFO policy.

        Args:
            key (str): The key under which the item is stored.
            item (any): The item to store in the cache.
        """
        if key and item:
            if len(self.cache_data) >= self.MAX_ITEMS:
                # Remove the first item (FIFO policy)y
                first_key = next(iter(self.cache_data))
                self.cache_data.pop(first_key)
                print(f"DISCARD: {first_key}")
            # Add the new key-value pair
            self.cache_data[key] = item

    def get(self, key):
        """Retrieve an item from the cache by key.

        Args:
            key (str): The key of the item to retrieve.

        Returns:
            The cached item, or None if the key is not in the cache or is None
        """
        return self.cache_data.get(key, None)