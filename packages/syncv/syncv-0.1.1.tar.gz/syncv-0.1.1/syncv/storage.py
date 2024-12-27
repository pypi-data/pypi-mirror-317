import json
import os

LOG_DIR = os.path.expanduser('~/.syncv_logs')
# LOG_DIR = './logs'

def get_log_path(name):
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    return os.path.join(LOG_DIR, f'{name}.json')

def load_log(name):
    path = get_log_path(name)
    if not os.path.exists(path):
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}
    
def save_log(name, data):
    path = get_log_path(name)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def clear_log(name):
    path = get_log_path(name)
    if os.path.exists(path):
        os.remove(path)

def get_peers():
    config = load_log('config')
    peers = config.get('peers', [])
    return peers

def add_peers(peer_code):
    config = load_log('config')
    peers = config.get('peers', [])
    if peer_code not in peers:
        peers.append(peer_code)
        config['peers'] = peers
        save_log('config', config)