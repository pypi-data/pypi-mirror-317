import time

import pyautogui

from .base import SearchService
from ..core.autoclip import AutoClip
from ..config import AutomationConfig
from ..core.autoweb import AutoWeb


class ChatGPTSearch(SearchService):
    """ChatGPT search implementation"""

    def format_query(self, query: str) -> str:
        return f"{query} start by saying [STARTING] and end by saying [ENDING]"

    def process_response(self, response: str) -> str:
        ist = response.find("[STARTING]")
        est = response.find("[ENDING]")
        text_v1 = response[response.find("[STARTING]", ist + 1) + 10:response.find("[ENDING]",
                                                                                   est + 1)].strip()
        return text_v1

    def perform_search(self, query: str,sleep=None) -> str:
        formatted_query = self.format_query(query)
        try:
            w, h = pyautogui.size()
            pyautogui.click(w - w/2, h - 60)
            time.sleep(2)
            AutoWeb.search(formatted_query)
            start_time = time.time()
            pyautogui.click(w - 50, h - 100)
            max_time = sleep or AutomationConfig.delays.chatgpt_text_process_time

            while True:
                time.sleep(AutomationConfig.delays.chatgpt_text_process_time)
                text = AutoClip.get_clipboard_content()

                if text.count("[ENDING]") > 1 or \
                    (time.time() - start_time > max_time):
                    return self.process_response(text)


        except Exception as e:
            print(f"Error performing search: {e}")
            return ""
