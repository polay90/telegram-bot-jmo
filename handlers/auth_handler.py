from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler, ContextTypes, CommandHandler, MessageHandler, filters
import re

# States untuk konversasi
PHONE_VERIFICATION, VERIFY_CODE, MAIN_MENU = range(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mulai bot dan minta nomor WhatsApp"""
    user = update.effective_user
    
    welcome_text = f"""
🤖 *Selamat Datang di Bot JMO Troubleshooting!*

Halo {user.first_name}! 👋

Bot ini dirancang untuk membantu Anda dengan masalah JMO Jamsostek.

📱 Silakan masukkan nomor WhatsApp Anda untuk verifikasi.
"""
    
    await update.message.reply_text(
        welcome_text,
        parse_mode='Markdown',
        reply_markup=ReplyKeyboardRemove()
    )
    
    return PHONE_VERIFICATION

async def receive_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Terima nomor WhatsApp"""
    phone = update.message.text.strip()
    
    # Validasi nomor telepon
    if not re.match(r'^(\+62|62|0)[0-9]{9,12}$', phone):
        await update.message.reply_text(
            "❌ Nomor tidak valid! Silakan gunakan format:\n"
            "✓ 62812345678\n"
            "✓ +62812345678\n"
            "✓ 0812345678"
        )
        return PHONE_VERIFICATION
    
    context.user_data['phone'] = phone
    context.user_data['user_id'] = update.effective_user.id
    
    await update.message.reply_text(
        f"✅ Nomor {phone} telah diterima.\n\n"
        f"📨 Kode verifikasi telah dikirim ke WhatsApp Anda.\n"
        f"Silakan masukkan kode 4 digit yang Anda terima:"
    )
    
    return VERIFY_CODE

async def verify_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Verifikasi kode"""
    code = update.message.text.strip()
    
    if not code.isdigit() or len(code) != 4:
        await update.message.reply_text(
            "❌ Kode tidak valid! Silakan masukkan 4 digit yang benar."
        )
        return VERIFY_CODE
    
    # Di sini bisa ditambahkan verifikasi dengan API WhatsApp
    context.user_data['verified'] = True
    
    await update.message.reply_text(
        "✅ Verifikasi berhasil!\n\n"
        "🎉 Anda berhasil login. Silakan pilih menu di bawah:"
    )
    
    return MAIN_MENU
