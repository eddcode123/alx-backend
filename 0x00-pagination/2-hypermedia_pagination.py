#!/usr/bin/env python3
""" Implementing hypermedia pagination."""

from typing import Tuple, List, Dict
import csv
import math


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """Calculate the start and end index for the given page and page size.

    Args:
        page (int): The page number (1-indexed).
        page_size (int): The number of items per page.

    Returns:
        Tuple[int, int]: A tuple containing the start index (inclusive) and
                         the end index (exclusive)."""
    start_index = (page - 1) * page_size
    end_index = page * page_size
    return (start_index, end_index)


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Get a page of data from the dataset.

    Args:
        page (int): The page number (1-indexed, must be > 0).
        page_size (int): The number of items per page (must be > 0).

    Returns:
        List[List]: A list of rows corresponding to the requested page.
        """
        # Assert that both parameters are integers
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0

        # use index range to get page range
        start_index, end_index = index_range(page, page_size)
        dataset = self.dataset()
        return dataset[start_index: end_index]
    
    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Return dataset as a dictionary
        :param page:
        :param page_size:
        :return:
        """
        total_pages = math.ceil(len(self.dataset()) / page_size)
        return {
            "page_size": page_size,
            "page": page,
            "data": self.get_page(page, page_size),
            "next_page": page + 1 if page + 1 <= total_pages else None,
            "prev_page": page - 1 if page > 1 else None,
            "total_pages": total_pages
        }
