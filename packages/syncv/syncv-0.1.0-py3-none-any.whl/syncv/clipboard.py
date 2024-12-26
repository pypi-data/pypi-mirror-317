import pyperclip
import threading
import time
from syncv.network import send_clipboard_content
from syncv.storage import load_log, save_log

def monitor_clipboard(unique_code):
    last_content = pyperclip.paste()

    log = load_log('clipboard')
    contents = log.get('contents', [])

    while True:
        try:
            cur_content = pyperclip.paste()
            if cur_content != last_content:
                last_content = cur_content
                send_clipboard_content(unique_code, cur_content)
                contents.append(cur_content)
                save_log('clipboard', {'contents': contents})
        except Exception as e:
            print(f'got an error when monitoring clipboard: {e}')
        time.sleep(0.5)

def start_clipboard_monitor(unique_code):
    thread = threading.Thread(target=monitor_clipboard, args=(unique_code,), daemon=True)
    thread.start()