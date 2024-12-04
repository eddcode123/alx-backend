#!/usr/bin/env python3
"""Basic cache"""

from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """BasicCache class inherits from BaseCaching
    and implements a simple caching system"""
    def put(self, key, item):
        """Add an item to the cache with a given key.

        Args:
            key (str): The key under which the item is stored.
            item (any): The item to store in the cache.
        """
        if key is not None or item is not None:
            self.cache_data[key] = item

    def get(self, key):
        """Retrieve an item from the cache by key.

        Args:
            key (str): The key of the item to retrieve.

        Returns:
            The cached item, or None if the key is not in the cache or is None
        """
        if key is None or key not in self.cache_data:
            return None

        return self.cache_data[key]
