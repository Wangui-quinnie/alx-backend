#!/usr/bin/env python3
""" LIFO Cache """


BaseCaching = __import__('base_caching').BaseCaching


class LIFOCache(BaseCaching):
    """ LIFOCache class """

    def __init__(self):
        """ Initialize LIFOCache """
        super().__init__()

    def put(self, key, item):
        """ Add an item in the cache """
        if key is None or item is None:
            return

        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            last_key = list(self.cache_data.keys())[-1]
            print("DISCARD: {}".format(last_key))
            del self.cache_data[last_key]

        self.cache_data[key] = item

    def get(self, key):
        """ Get an item from cache """
        if key is None or key not in self.cache_data:
            return None

        return self.cache_data[key]
