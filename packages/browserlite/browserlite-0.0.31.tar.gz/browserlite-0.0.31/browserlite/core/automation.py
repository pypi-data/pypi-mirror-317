from typing import Dict, Optional, Literal
import pyautogui
from ..services import ChatGPTSearch,HuggingChatSearch,GoogleSearch
from ..core.autoweb import AutoWeb

SearchServiceType = Literal["openai","google","huggingchat","chatgpt"]

_SERVICE_NAME_MAP = {
    "chatgptsearch":"chatgpt",
    "chatgpt":"chatgpt",
    "openai":"chatgpt",
    "huggingchat":"huggingchat"
}

class AutomationManager:
    """Main automation manager class"""

    def __init__(self):
        pyautogui.FAILSAFE = True
        self.services: Dict= {
            "chatgpt": ChatGPTSearch(),
            "huggingchat": HuggingChatSearch(),
            "google":GoogleSearch()
        }

    def execute_search(self, query: str, service_name: SearchServiceType="google",
                       browser="microsoft-edge-stable",
                       base_url:str|None = None,
                       sleep:int|None=None) -> Optional[str]:
        """Execute a search using the specified service"""
        name = _SERVICE_NAME_MAP.get(service_name, "google")

        # if service_name=="chatgpt":
        #     query = f"https://www.{name}.com/search?q={query}"

        service:HuggingChatSearch|ChatGPTSearch = self.services.get(name)

        if not service:
            print(f"Service {service_name} not found")
            return None

        if not AutoWeb.open(base_url=base_url,
                            browser_name=browser):
            return None

        try:
            result = service.perform_search(query=query,
                                            sleep=sleep)
            return result
        finally:
            AutoWeb.close()

