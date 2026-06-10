import requests
import json
from config import WHATSAPP_TOKEN, WHATSAPP_PHONE_ID  # tambahkan ke config.py

def send_whatsapp_message(to_phone: str, message: str):
    """Kirim pesan WhatsApp"""
    url = f"https://graph.facebook.com/v20.0/{WHATSAPP_PHONE_ID}/messages"
    
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messaging_product": "whatsapp",
        "to": to_phone,
        "type": "text",
        "text": {"body": message}
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        return response.json()
    except Exception as e:
        print(f"WhatsApp Error: {e}")
        return None
