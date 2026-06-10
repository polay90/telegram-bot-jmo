import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackQueryHandler
from config import TELEGRAM_BOT_TOKEN
from handlers.auth_handler import (
    start, receive_phone, verify_code, 
    PHONE_VERIFICATION, VERIFY_CODE, MAIN_MENU
)
from handlers.menu_handler import (
    show_main_menu, show_kode_040_menu, show_suspend_menu, show_unlock_menu
)
from handlers.jmo_handler import (
    kode_040_start, kode_040_email, kode_040_password, kode_040_kpj,
    suspend_kpj_start, suspend_email, suspend_password,
    unlock_biometrik_start, unlock_nama_ibu, unlock_nama_perusahaan, 
    unlock_email, unlock_peserta,
    KODE_040_EMAIL, KODE_040_PASSWORD, KODE_040_KPJ,
    SUSPEND_EMAIL, SUSPEND_PASSWORD,
    UNLOCK_NAMA_IBU, UNLOCK_NAMA_PERUSAHAAN, UNLOCK_EMAIL, UNLOCK_PESERTA
)

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Handler untuk pesan teks
async def handle_message(update, context):
    """Handle pesan dari user"""
    text = update.message.text
    
    if text == "🔧 Kode 040":
        await show_kode_040_menu(update, context)
    elif text == "🔐 Suspend Nomor KPJ":
        await show_suspend_menu(update, context)
    elif text == "🔑 Unlock Biometrik":
        await show_unlock_menu(update, context)
    elif text == "❓ Bantuan":
        await update.message.reply_text(
            "📞 *Hubungi Kami*\n\n"
            "Jika ada pertanyaan, hubungi:\n"
            "@play1990",
            parse_mode='Markdown'
        )

# Handler untuk callback query
async def handle_callback(update, context):
    """Handle button callbacks"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'kode_040_start':
        return await kode_040_start(update, context)
    elif query.data == 'suspend_kpj_start':
        return await suspend_kpj_start(update, context)
    elif query.data == 'unlock_biometrik_start':
        return await unlock_biometrik_start(update, context)
    elif query.data == 'back_to_menu':
        await show_main_menu(update, context)

def main():
    """Start bot"""
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Conversation handler untuk auth
    auth_conv = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            PHONE_VERIFICATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_phone)],
            VERIFY_CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, verify_code)],
            MAIN_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)],
        },
        fallbacks=[]
    )
    
    # Conversation handler untuk Kode 040
    kode_040_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(kode_040_start, pattern='kode_040_start')],
        states={
            KODE_040_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, kode_040_email)],
            KODE_040_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, kode_040_password)],
            KODE_040_KPJ: [MessageHandler(filters.TEXT & ~filters.COMMAND, kode_040_kpj)],
        },
        fallbacks=[]
    )
    
    # Conversation handler untuk Suspend KPJ
    suspend_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(suspend_kpj_start, pattern='suspend_kpj_start')],
        states={
            SUSPEND_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, suspend_email)],
            SUSPEND_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, suspend_password)],
        },
        fallbacks=[]
    )
    
    # Conversation handler untuk Unlock Biometrik
    unlock_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(unlock_biometrik_start, pattern='unlock_biometrik_start')],
        states={
            UNLOCK_NAMA_IBU: [MessageHandler(filters.TEXT & ~filters.COMMAND, unlock_nama_ibu)],
            UNLOCK_NAMA_PERUSAHAAN: [MessageHandler(filters.TEXT & ~filters.COMMAND, unlock_nama_perusahaan)],
            UNLOCK_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, unlock_email)],
            UNLOCK_PESERTA: [MessageHandler(filters.TEXT & ~filters.COMMAND, unlock_peserta)],
        },
        fallbacks=[]
    )
    
    # Tambahkan handlers
    application.add_handler(auth_conv)
    application.add_handler(kode_040_conv)
    application.add_handler(suspend_conv)
    application.add_handler(unlock_conv)
    application.add_handler(CallbackQueryHandler(handle_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Start bot
    application.run_polling()
    print("✅ Bot sudah berjalan!")

if __name__ == '__main__':
    main()
