import time
import pyautogui
import pyperclip


class AutoClip:
    """Class for handling text operations"""

    @classmethod
    def select_all(cls) -> bool:
        try:
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(1)
            return True
        except Exception as e:
            print(f"Error selecting text: {e}")
            return False

    @classmethod
    def copy(cls) -> bool:
        try:
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(1)
            return True
        except Exception as e:
            print(f"Error copying text: {e}")
            return False

    @classmethod
    def get_clipboard_content(cls) -> str:
        cls.select_all()
        cls.copy()
        return pyperclip.paste()
