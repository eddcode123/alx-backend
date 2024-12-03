#!/usr/bin/env python3
""" Implementing hypermedia pagination."""

from typing import Tuple, List, Dict, Any
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
        Return a paginated dataset as a dictionary with additional metadata.

        Args:
            page (int): The current page number (1-indexed).
            page_size (int): The number of items per page.

        Returns:
            Dict[str, Any]: A dictionary containing:
                - "page_size": Number of items per page.
                - "page": Current page number.
                - "data": List of items on the current page.
                - "next_page": Next page number
                                (or None if no next page).
                - "prev_page": Previous page number
                                (or None if no previous page).
                - "total_pages": Total number of pages.
        """
        # Assert input validity
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0

        # Calculate total number of pages
        dataset = self.dataset()
        total_items = len(dataset)
        total_pages = math.ceil(total_items / page_size)

        # Build the response dictionary
        return {
            "page_size": page_size,
            "page": page,
            "data": self.get_page(page, page_size),
            "next_page": page + 1 if page < total_pages else None,
            "prev_page": page - 1 if page > 1 else None,
            "total_pages": total_pages
        }

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """
        Returns a dictionary containing paginated data with metadata.

        Args:
            index (int): The starting index (0-based).
            page_size (int): The number of items to retrieve.

        Returns:
            Dict: A dictionary containing:
                - "index": The starting index.
                - "data": The list of items for the page.
                - "page_size": The size of the page.
                - "next_index": The next valid index after the page.

        Raises:
            AssertionError: If `index` or `page_size` is not an integer.
                            If `index` is out of bounds of the dataset.
        """
        # Validate input
        assert isinstance(index, int), "index must be an integer"
        assert isinstance(page_size, int)
        csv = self.indexed_dataset()
        csv_size = len(csv)
        assert 0 <= index < csv_size

        data = []
        current_index = index

        # Gather data, skipping missing entries
        for _ in range(page_size):
            while current_index < csv_size and current_index not in csv:
                current_index += 1
            if current_index < csv_size:
                data.append(csv[current_index])
                current_index += 1
            else:
                break

        return {
            "index": index,
            "data": data,
            "page_size": len(data),
            "next_index": current_index if current_index < csv_size else None
        }
