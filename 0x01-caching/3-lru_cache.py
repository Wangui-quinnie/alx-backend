#!/usr/bin/env python3
""" LRU Cache """


from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """ LRUCache class """

    def __init__(self):
        """ Initialize LRUCache """
        super().__init__()
        self.lru_keys = []

    def put(self, key, item):
        """ Add an item in the cache """
        if key is None or item is None:
            return

        if len(self.cache_data) >= self.MAX_ITEMS:
            if key not in self.cache_data:
                discarded_key = self.lru_keys.pop(0)
                if discarded_key in self.cache_data:
                    del self.cache_data[discarded_key]
                    print("DISCARD: {}".format(discarded_key))

        self.cache_data[key] = item
        if key in self.lru_keys:
            self.lru_keys.remove(key)
        self.lru_keys.append(key)

    def get(self, key):
        """ Get an item from cache """
        if key is None or key not in self.cache_data:
            return None

        if key in self.lru_keys:
            self.lru_keys.remove(key)
        self.lru_keys.append(key)

        return self.cache_data[key]
