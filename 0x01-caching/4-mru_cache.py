#!/usr/bin/env python3
"""MRU caching policy"""

from base_caching import BaseCaching
from typing import Union, Any


class MRUCache(BaseCaching):
    """MRUCache inherits from BaseCaching
    and implements a LRu caching system"""

    def __init__(self):
        super().__init__()
        self.key_order = []

    def put(self, key: str, item: Any):
        """ Add an item to the cache with MRU policy

        Args:
            key (str): The key under which the item is stored.
            item (Any): The item to store in the cache.
        """
        if key and item:
            # check if key exist in key_order
            if key in self.key_order:
                # remove key from key _order
                self.key_order.remove(key)
            elif len(self.cache_data) >= self.MAX_ITEMS:
                # if cache is full free memory
                mru_key = self.key_order.pop(-1)
                print(f"DISCARD: {mru_key}")
                self.cache_data.pop(mru_key)
            self.cache_data[key] = item
            self.key_order.append(key)

    def get(self, key: str) -> Union[Any, None]:
        """Retrieve an item from the cache by key.

        Args:
            key (str): The key of the item to retrieve.

        Returns:
            The cached item, or None if the key is not in the cache or is None
        """
        if key in self.cache_data:
            self.key_order.remove(key)
            self.key_order.append(key)
            return self.cache_data[key]
        return None
