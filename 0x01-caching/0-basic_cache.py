#!/usr/bin/env python3
""" BasicCache module
"""


from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """ BasicCache class that inherits from BaseCaching and
    represents a caching system.
    """

    def put(self, key, item):
        """
        Assigns the item value to the key in the cache_data dictionary.

        Args:
            key: The key to be used for storing the item.
            item: The item to be stored in the cache.
        """
        if key is None or item is None:
            return
        self.cache_data[key] = item

    def get(self, key):
        """
        Returns the value associated with the given key from the
        cache_data dictionary.

        Args:
            key: The key to be used for retrieving the value.

        Returns:
            The value associated with the given key, or None if the key is
            None or not found in the cache.
        """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
