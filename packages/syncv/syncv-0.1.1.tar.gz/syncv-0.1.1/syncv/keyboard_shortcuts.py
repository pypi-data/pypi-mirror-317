import os
import sys
import pyperclip
from pynput import keyboard
from syncv.network import send_clipboard_content


def is_headless():
    """Detect if the environment is headless."""
    return os.environ.get("DISPLAY") is None and os.environ.get("WAYLAND_DISPLAY") is None


def on_copy(code):
    try:
        contents = pyperclip.paste()
        send_clipboard_content(code, contents)
        print(f"Copied: {contents}")
    except Exception as e:
        print(f"Error in on_copy: {e}")


def on_paste():
    try:
        # Simulate paste operation
        print("Paste triggered.")
        pyperclip.paste()
    except Exception as e:
        print(f"Error in on_paste: {e}")


def monitor_clipboard(unique_code):
    """Poll clipboard changes for headless environments."""
    previous_content = pyperclip.paste()
    print("Starting clipboard monitor for headless environment...")
    while True:
        try:
            current_content = pyperclip.paste()
            if current_content != previous_content:
                previous_content = current_content
                send_clipboard_content(unique_code, current_content)
                print(f"Clipboard updated: {current_content}")
        except Exception as e:
            print(f"Error monitoring clipboard: {e}")


def on_press(key, unique_code):
    """Handle key press in GUI environments."""
    try:
        if key == keyboard.Key.cmd:
            # Pressed command key; wait for 'c' or 'v'
            print("Command key pressed.")
    except Exception as e:
        print(f"Error in on_press: {e}")


def on_release(key, unique_code):
    """Handle key release in GUI environments."""
    try:
        if key == keyboard.KeyCode.from_char('c'):
            on_copy(unique_code)
        elif key == keyboard.KeyCode.from_char('v'):
            on_paste()
        return False  # Stop listener after handling
    except Exception as e:
        print(f"Error in on_release: {e}")


def setup_hotkeys(unique_code):
    """Setup hotkeys or clipboard monitoring based on the environment."""
    if is_headless():
        # In headless environments, monitor clipboard instead of listening to hotkeys
        print("Headless mode detected: Using clipboard monitoring.")
        monitor_clipboard(unique_code)
    else:
        # GUI environment: Set up hotkeys
        print("GUI environment detected: Setting up hotkeys.")
        try:
            with keyboard.Listener(on_press=lambda k: on_press(k, unique_code),
                                   on_release=lambda k: on_release(k, unique_code)) as listener:
                listener.join()
        except Exception as e:
            print(f"Error setting up hotkeys: {e}")