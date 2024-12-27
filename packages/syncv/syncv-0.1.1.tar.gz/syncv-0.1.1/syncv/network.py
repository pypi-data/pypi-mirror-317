import requests
import threading
import pyperclip
import json
from flask import Flask, request, jsonify
from syncv.storage import load_log, save_log, get_peers, add_peers

app = Flask(__name__)
cur_unique_code = None
peers = set()

def bind_device_network(code, unique_code):
    if code:
        add_peers(code)
        return True
    return False

def start_server(unique_code):
    global cur_unique_code
    cur_unique_code = unique_code

    @app.route('/clipboard', methods=['POST'])
    def receive_clipboard():
        data = request.get_json()
        code = data.get('code')
        content = data.get('content')
        
        if code != cur_unique_code:
            return jsonify({'status': 'Unauthorized'}), 403
        
        if content:
            # pass content to clipboard
            pyperclip.copy(content)

            log = load_log('clipboard')
            contents = log.get('contents', [])
            contents.append(contents)
            save_log('clipboard', {'contents': contents})
            return jsonify({'status': 'OK'}), 200
        return jsonify({'status': 'No content received'}), 400
        
    # start Flask
    thread = threading.Thread(target=lambda: app.run(port=5000, debug=False, use_reloader=False), daemon=True)
    thread.start()

def send_clipboard_content(unique_code, content):
    peers = get_peers()
    for peer in peers:
        url = f'http://{peer}/clipboard'
        try:
            response = requests.post(url, json={'code': unique_code, 'content': content}, timeout=5)
            if response.status_code != 200:
                print(f"Failed to send to {peer}: {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"Error sending to {peer}: {e}")

def discover_peers():
    pass