# sync/core.py

import uuid
import threading
import time
from syncv.storage import load_log, save_log, clear_log, get_peers
from syncv.network import bind_device_network, send_clipboard_content, start_server
from syncv.clipboard import start_clipboard_monitor
from syncv.keyboard_shortcuts import setup_hotkeys

def initialize():
    code = load_log('config').get('unique_code')
    if code:
        return f'Already initialized. Your unique code is: {code}'

    unique_code = str(uuid.uuid4())
    # 保存唯一代码到本地配置
    save_log('config', {'unique_code': unique_code})
    # 启动网络服务或绑定设备
    start_server(unique_code)
    return unique_code

def bind_device(code):
    unique_code = load_log('config').get('unique_code')
    if not unique_code:
        # 如果本地没有初始化，不能绑定
        return False
    return bind_device_network(code, unique_code)

def get_binded_peers():
    return get_peers()

def list_contents():
    log = load_log('clipboard')
    return log.get('contents', [])

def clear_contents():
    clear_log('clipboard')

def start_service():
    config = load_log('config')
    unique_code = config.get('unique_code')
    if not unique_code:
        print("Service not initialized. Please run 'sync init' first.")
        return

    # 启动剪贴板监控
    start_clipboard_monitor(unique_code)

    # 启动键盘快捷键
    setup_hotkeys(unique_code)

    # 启动设备发现（如果实现）
    # 可以在此处添加自动发现或其他功能

    # 保持主线程运行
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Sync service stopped.")