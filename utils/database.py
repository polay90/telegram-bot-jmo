import json
import os
from datetime import datetime

USER_DATA_FILE = 'user_data.json'

def save_user_data(user_id, data):
    """Simpan data pengguna"""
    users = load_all_users()
    users[str(user_id)] = {
        **data,
        'timestamp': datetime.now().isoformat()
    }
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def load_all_users():
    """Muat semua data pengguna"""
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def get_user_data(user_id):
    """Dapatkan data pengguna spesifik"""
    users = load_all_users()
    return users.get(str(user_id), {})
