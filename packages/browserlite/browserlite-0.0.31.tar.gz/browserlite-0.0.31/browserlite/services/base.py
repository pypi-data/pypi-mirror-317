from abc import ABC, abstractmethod


class SearchService(ABC):
    """Abstract base class for search services"""

    @abstractmethod
    def format_query(self, query: str) -> str:
        """Format the search query according to service requirements"""
        pass

    @abstractmethod
    def process_response(self, response: str) -> str:
        """Process the response from the search service"""
        pass

    @abstractmethod
    def perform_search(self, query: str) -> str:
        """Perform the search operation"""
        pass

