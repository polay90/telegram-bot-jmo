from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from enum import Enum

class MenuState(Enum):
    KODE_040 = "kode_040"
    SUSPEND_KPJ = "suspend_kpj"
    UNLOCK_BIOMETRIK = "unlock_biometrik"

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tampilkan menu utama"""
    keyboard = [
        [KeyboardButton("🔧 Kode 040")],
        [KeyboardButton("🔐 Suspend Nomor KPJ")],
        [KeyboardButton("🔑 Unlock Biometrik")],
        [KeyboardButton("❓ Bantuan")]
    ]
    
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    
    menu_text = """
╔═══════════════════════════════════╗
║  🎯 MENU UTAMA - JMO TROUBLESHOOTING  ║
╚═══════════════════════════════════╝

Pilih salah satu layanan di bawah:

🔧 *Kode 040* - Solusi untuk error kode 040
🔐 *Suspend Nomor KPJ* - Buka suspend nomor KPJ Anda
🔑 *Unlock Biometrik* - Unlock biometrik Jamsostek

Silakan pilih opsi yang Anda butuhkan:
"""
    
    await update.message.reply_text(
        menu_text,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def show_kode_040_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menu untuk Kode 040"""
    keyboard = [
        [InlineKeyboardButton("✅ Lanjutkan", callback_data='kode_040_start')],
        [InlineKeyboardButton("⬅️ Kembali", callback_data='back_to_menu')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = """
╔════════════════════════════════════╗
║     🔧 SOLUSI KODE 040              ║
╚════════════════════════════════════╝

Proses penyelesaian Kode 040:

1️⃣ Login ke Akun Jamsostek Mobile
2️⃣ Masukkan Email dan Password
3️⃣ Lakukan Klaim Langsung
4️⃣ Isi Tahun KPJ
5️⃣ Proses akan berjalan ±60 menit
6️⃣ Tunggu hingga proses selesai

⏱️ Estimasi waktu: *60 menit*

Siap melanjutkan?
"""
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            text,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            text,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )

async def show_suspend_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menu untuk Suspend KPJ"""
    keyboard = [
        [InlineKeyboardButton("✅ Lanjutkan", callback_data='suspend_kpj_start')],
        [InlineKeyboardButton("⬅️ Kembali", callback_data='back_to_menu')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = """
╔════════════════════════════════════╗
║   🔐 LEPAS SUSPEND NOMOR KPJ        ║
╚════════════════════════════════════╝

Proses pelepasan suspend:

1️⃣ Login ke Akun Jamsostek Mobile
2️⃣ Masukkan Email dan Password
3️⃣ Klik Tombol Lepas Suspend
4️⃣ Proses akan berjalan ±45 menit
5️⃣ Tunggu hingga proses selesai

⏱️ Estimasi waktu: *45 menit*

Siap melanjutkan?
"""
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            text,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            text,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )

async def show_unlock_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menu untuk Unlock Biometrik"""
    keyboard = [
        [InlineKeyboardButton("✅ Lanjutkan", callback_data='unlock_biometrik_start')],
        [InlineKeyboardButton("⬅️ Kembali", callback_data='back_to_menu')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = """
╔════════════════════════════════════╗
║    🔑 UNLOCK BIOMETRIK JAMSOSTEK    ║
╚════════════════════════════════════╝

Proses unlock biometrik:

1️⃣ Masukkan Nama Ibu Kandung
2️⃣ Masukkan Nama Perusahaan
3️⃣ Masukkan Gmail Aktif
4️⃣ Masukkan Nomor Peserta (NIPP)
5️⃣ Data akan diproses dalam 1x24 jam

⏱️ Estimasi waktu: *1 hari kerja*

Siap melanjutkan?
"""
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            text,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            text,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
