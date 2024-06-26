#!/usr/bin/env python3
""" LFU Cache """


from base_caching import BaseCaching
from collections import defaultdict


class LFUCache(BaseCaching):
    """ LFUCache class """

    def __init__(self):
        """ Initialize LFUCache """
        super().__init__()
        self.frequency = defaultdict(int)
        self.keys_by_frequency = defaultdict(list)
        self.min_frequeny = 0

    def put(self, key, item):
        """ Add an item in the cache """
        if key is not None and item is not None:
            if len(self.cache_data) >= self.MAX_ITEMS:
                if self.min_frequency in self.keys_by_frequency:
                    discarded_key = \
                        self.keys_by_frequency[self.min_frequency].pop(0)
                    if len(self.keys_by_frequency[self.min_frequency]) == 0:
                        del self.keys_by_frequency[self.min_frequency]
                    del self.cache_data[discarded_key]
                    del self.frequency[discarded_key]
                    print(f"DISCARD: {discarded_key}")
            self.cache_data[key] = item
            self.frequency[key] += 1
            self.keys_by_frequency[self.frequency[key]].append(key)
            self.min_frequency = min(self.frequency.values())

    def get(self, key):
        """
        This method returns value of data returned to key
        """
        if key is not None and key in self.cache_data:
            self.frequency[key] += 1
            self.keys_by_frequency[self.frequency[key] - 1].remove(key)
            if len(self.keys_by_frequency[self.frequency[key] - 1]) == 0:
                del self.keys_by_frequency[self.frequency[key] - 1]
                if self.min_frequency == self.frequency[key]:
                    self.min_frequency += 1
            self.keys_by_frequency[self.frequency[key]].append(key)
            return self.cache_data[key]
        return None
