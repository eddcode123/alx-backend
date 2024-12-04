#!/usr/bin/env python3
"""LIFO caching policy"""

from base_caching import BaseCaching
from typing import Any


class LIFOCache(BaseCaching):
    """LIFOCache class inherits from BaseCaching
    and implements a LIFO caching system"""
    def __init__(self):
        """Initialize the LIFOCache instance."""
        super().__init__()

    def put(self, key: str, item: Any):
        """ Add an item to the cache with LIFO policy

        Args:
            key (str): The key under which the item is stored.
            item (Any): The item to store in the cache.
        """
        if key and item:
            if len(self.cache_data) >= self.MAX_ITEMS:
                # Get the last added key (LIFO policy)
                last_key = next(reversed(self.cache_data))
                self.cache_data.pop(last_key)
                print(f"DISCARD: {last_key}")
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
