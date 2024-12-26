import time
from typing import Optional

import pyautogui
from .base import SearchService
from ..core.autoclip import AutoClip
from ..config import AutomationConfig
from ..core.autoweb import AutoWeb


class GoogleSearch(SearchService):
    """ChatGPT search implementation"""


    def format_query(self, query: str) -> str:
        return query

    def process_response(self, response: str) -> str:
        return response

    def perform_search(self, query: str,sleep:Optional[int]=None) -> str:
        query = self.format_query(query)

        try:
            AutoWeb.search(query)
            text = AutoClip.get_clipboard_content()
            return text

        except Exception as e:
            print(f"Error performing search: {e}")
            return ""
