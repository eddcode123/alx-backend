#!/usr/bin/env python3
"""LFU cache policy"""

from base_caching import BaseCaching
from typing import Union, Any


class LFUCache(BaseCaching):
    """LFUCache class inherits from BaseCaching
    and implements a LFU caching system
    """
    def __init__(self):
        super().__init__()
        self.frequency_and_key_order = {}

    def put(self, key: str, item: Any):
        """
        Add an item to the cache with LFU policy

        Args:
            key (str): The key under which the item is stored.
            item (Any): The item to store in the cache.
        """
        if key is None or item is None:
            return

        if key in self.cache_data:
            # If the key exists, update the item and frequency
            self.cache_data[key] = item
            self.frequency_and_key_order[key] += 1
        else:
            # If the key doesn't exist and the cache is full, evict an item
            if len(self.cache_data) >= self.MAX_ITEMS:
                # Find the least frequently used item(s)
                min_freq = min(self.frequency_and_key_order.values())
                lfu_keys = [
                    k
                    for k, v in self.frequency_and_key_order.items()
                    if v == min_freq
                    ]

                # Evict the least recently used among LFU items
                key_to_evict = lfu_keys[0]
                del self.cache_data[key_to_evict]
                del self.frequency_and_key_order[key_to_evict]
                print(f"DISCARD: {key_to_evict}")

            # Add the new key and set frequency to 1
            self.cache_data[key] = item
            self.frequency_and_key_order[key] = 1

    def get(self, key: str) -> Union[Any, None]:
        """Retrieve an item from the cache by key.

        Args:
            key (str): The key of the item to retrieve.

        Returns:
            The cached item, or None if the key is not in the cache or is None
        """
        if key is None or key not in self.cache_data:
            return None

        # Increment frequency count for the accessed key
        self.frequency_and_key_order[key] += 1
        return self.cache_data[key]
