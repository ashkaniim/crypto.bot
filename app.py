# app.py
import os
import logging
from datetime import datetime
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# --- فایل keep_alive برای Replit / UptimeRobot ---
from keep_alive import keep_alive

keep_alive()  # اینو همینجا اضافه می‌کنیم تا Flask server اجرا بشه

# --- Token bot ---
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # یا مستقیماً TOKEN رو بذار، بهتره با env

# --- فعال کردن Logging ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# --- دستور /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = """
🤖 به ربات گارد سیگنال خوش آمدید ✅
برای دریافت سیگنال، مثلا بنویسید:
/signal BTCUSDT 4h
"""
    await update.message.reply_text(welcome_message)


# --- دستور /signal (نمونه ساده) ---
async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.split()
    if len(user_input) < 3:
        await update.message.reply_text("لطفا مانند مثال /signal BTCUSDT 4h وارد کنید.")
        return

    symbol = user_input[1].upper()
    timeframe = user_input[2].lower()

    # نمونه پاسخ ساده، می‌تونی df و تحلیل واقعی بذاری
    message = f"📊 سیگنال {symbol} | تایم‌فریم: {timeframe} آماده است!"
    await update.message.reply_text(message)


# --- ساخت اپلیکیشن تلگرام ---
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.Regex(r"^/signal "), signal))

print("ربات در حال اجراست...")
app.run_polling()
