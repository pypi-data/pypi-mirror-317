import os
import sys
import time
import webbrowser

import pyautogui
from browserlite.config import AutomationConfig
from loguru import logger


class AutoWeb:
    """Automates browser operations such as opening, closing, searching, and entering text."""

    @classmethod
    def open(cls, base_url=None, browser_name=None) -> bool: #browser_name: [
        try:
            webbrowser.open(base_url)
            time.sleep(AutomationConfig.delays.edge_open_delay)
            logger.debug('Opened using python webbrowser')
            return True
        except Exception as e:
            logger.debug(f"Error opening webbrowser : {e}")
            try:
                os.system(browser_name)
                time.sleep(AutomationConfig.delays.edge_open_delay)
                if base_url:
                    pyautogui.write(base_url)
                    pyautogui.press('enter')
                logger.debug('Opened using Os browser')
                return True
            except Exception as e:
                logger.debug(f"Error opening Edge: {e}")
                return False

    @classmethod
    def close(cls) -> bool:
        try:
            pyautogui.hotkey('ctrl', 'w')
            return True
        except Exception as e:
            logger.error(f"Error closing browser: {e}")
            return False

    @classmethod
    def search(cls, search_text):
        """Type and search for given text"""
        try:
            pyautogui.write(search_text)
            pyautogui.press('enter')
            time.sleep(AutomationConfig.delays.search_delay)
            return True
        except Exception as e:
            logger.error(f"Error performing search: {e}")
            return False
