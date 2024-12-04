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
        self.keys_order = []

    def put(self, key: str, item: Any):
        """ Add an item to the cache with LIFO policy

        Args:
            key (str): The key under which the item is stored.
            item (Any): The item to store in the cache.
        """
        if key and item:
            if key in self.cache_data:
                # If key already exists, update
                # its value and move it to the end
                self.keys_order.remove(key)
            elif len(self.cache_data) >= self.MAX_ITEMS:
                # Remove the last added key from the ordered list
                last_key = self.keys_order.pop(-1)
                self.cache_data.pop(last_key)
                print(f"DISCARD: {last_key}")

            # Add the new key-value pair
            self.cache_data[key] = item
            self.keys_order.append(key)

    def get(self, key):
        """Retrieve an item from the cache by key.

        Args:
            key (str): The key of the item to retrieve.

        Returns:
            The cached item, or None if the key is not in the cache or is None
        """
        return self.cache_data.get(key, None)
