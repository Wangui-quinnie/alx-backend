#!/usr/bin/env python3
""" FIFOCache module
"""


from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """ FIFOCache class that inherits from BaseCaching and represents a caching
    system using FIFO algorithm.
    """

    def __init__(self):
        """
        Initializes the FIFOCache instance by calling the parent
        class's init method.
        """
        super().__init__()

    def put(self, key, item):
        """
        Assigns the item value to the key in the cache_data dictionary.

        If the number of items in self.cache_data is higher than BaseCaching.
        MAX_ITEMS,
        the first item put in cache (FIFO algorithm) will be discarded.

        Args:
            key: The key to be used for storing the item.
            item: The item to be stored in the cache.
        """
        if key is None or item is None:
            return
        if len(self.cache_data) >= self.MAX_ITEMS:
            first_key = next(iter(self.cache_data))
            print("DISCARD:", first_key)
            del self.cache_data[first_key]
        self.cache_data[key] = item

    def get(self, key):
        """
        Returns the value associated with the given key from the cache_data
        dictionary.

        Args:
            key: The key to be used for retrieving the value.

        Returns:
            The value associated with the given key, or None if the key is
            None or not found in the cache.
        """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
