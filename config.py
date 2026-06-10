import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID', '@play1990')
JAMSOSTEK_API_URL = os.getenv('JAMSOSTEK_API_URL', 'https://api.jamsostek.go.id')
WHATSAPP_TOKEN = "JCXAf-vzhaSiyd0SQvfKlzd6AjU"          # Dari Meta
WHATSAPP_PHONE_ID = "1556975352706684"             # Dari Meta
WHATSAPP_ADMIN_NUMBER = "62895423349883"                # Nomor admin WhatsApp
