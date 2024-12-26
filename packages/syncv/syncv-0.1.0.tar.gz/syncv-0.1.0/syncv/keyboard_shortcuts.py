import keyboard
import pyperclip
from syncv.network import send_clipboard_content
from syncv.storage import load_log


def on_copy(code):
    try:
        contents = pyperclip.paste()
        send_clipboard_content(code, contents)
    except Exception as e:
        print(f"Error in on_copy: {e}")

def on_paste(code):
    try:
        keyboard.press_and_release('ctrl+v')
    except Exception as e:
        print(f"Error in on_paste: {e}")

def setup_hotkeys(unique_code):
    keyboard.add_hotkey('ctrl+c', lambda: on_copy(unique_code))
    keyboard.add_hotkey('ctrl+v', lambda: on_paste(unique_code))