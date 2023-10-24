#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
from typing import List, Dict


class Server:
    """
    Server class to paginate a database of popular baby names
    """

    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """
        Initialize the Server object with dataset
        and indexed dataset attributes
        """
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """
        Retrieve and cache the dataset from a CSV file,
        skipping the header row

        Returns:
            List[List]: The cached dataset as a list of lists
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """
        Create an indexed dataset starting from position 0

        Returns:
            Dict[int, List]: The indexed dataset as a dictionary
            with sorting positions as keys
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
        Get a hypermedia index for pagination

        Args:
            index (int): The current start index of the return page
            page_size (int): The size of the current page

        Returns:
            Dict: A dictionary with key-value pairs
            (index, next_index, page_size, data)
        """
        # Check if index and page_size are integers
        assert type(index) == int
        assert type(page_size) == int

        # Get the indexed dataset and its size
        csv = self.indexed_dataset()
        csv_size = len(csv)

        # Check if the index is in a valid range
        assert 0 <= index < csv_size

        data = []  # Store the data for the current page
        _next = index  # Initialize the next index

        # Iterate to fetch data for the current page
        for _ in range(page_size):
            while not csv.get(_next):
                _next += 1
            data.append(csv.get(_next))
            _next += 1

        return {
            "index": index,
            "data": data,
            "page_size": page_size,
            "next_index": _next
        }
