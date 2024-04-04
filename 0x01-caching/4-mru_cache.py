#!/usr/bin/env python3
""" MRU Cache """


from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """ MRUCache class """

    def __init__(self):
        """ Initialize MRUCache """
        super().__init__()
        self.mru_keys = []

    def put(self, key, item):
        """ Add an item in the cache """
        if key is None or item is None:
            return

        if len(self.cache_data) >= self.MAX_ITEMS:
            if key not in self.cache_data:
                discarded_key = self.mru_keys.pop(-1)
                if discarded_key in self.cache_data:
                    del self.cache_data[discarded_key]
                    print("DISCARD: {}".format(discarded_key))

        self.cache_data[key] = item
        if key in self.mru_keys:
            self.mru_keys.remove(key)
        self.mru_keys.append(key)

    def get(self, key):
        """ Get an item from cache """
        if key is None or key not in self.cache_data:
            return None

        if key in self.mru_keys:
            self.mru_keys.remove(key)
        self.mru_keys.append(key)

        return self.cache_data[key]
