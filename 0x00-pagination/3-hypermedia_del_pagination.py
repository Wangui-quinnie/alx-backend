#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""


import csv
import math
from typing import List, Dict


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """
        Returns a dictionary containing hypermedia metadata for the
        specified index.

        Args:
            index (int, optional): Index of the first item in the
            current page. Defaults to None.
            page_size (int, optional): Number of items per page.
            Defaults to 10.

        Returns:
            Dict: Dictionary containing hypermedia metadata.
        """
        assert isinstance(index, int) and index >= 0, \
            "Index must be a non-negative integer"
        assert isinstance(page_size, int) and page_size > 0, \
            "Page size must be a positive integer"

        indexed_dataset = self.indexed_dataset()

        if index is None:
            index = 0

        assert index < len(indexed_dataset), "Index out of range"

        data = [indexed_dataset[i] for i in
                range(index, min(index + page_size, len(indexed_dataset)))]
        next_index = min(index + page_size, len(indexed_dataset))

        return {
            "index": index,
            "data": data,
            "page_size": page_size,
            "next_index": next_index if next_index < len(indexed_dataset)
            else None
        }
