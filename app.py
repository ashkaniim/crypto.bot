import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from data_source import fetch_ohlcv
from indicators import add_indicators
from signal_handler import generate_signal
from config import TOKEN
from keep_alive import keep_alive

# حذف webhook قدیمی
requests.get(f"https://api.telegram.org/bot{TOKEN}/deleteWebhook")

# Keep-Alive برای Replit
keep_alive()


# دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = """
درود به ربات گارد سیگنال خوش آمدید ✅
این ربات از تمام ارزهای صرافی بایننس پشتیبانی میکند.

ارز مورد نظر را مانند مثال زیر بنویسید و منتظر بمانید:
/signal BTCUSDT 4h

توضیح: سیگنال‌ها بر اساس حجم، خطوط حمایت/مقاومت، EMA200 و سایر اندیکاتورها ارائه می‌شوند.

-------------------------
Welcome to Guard Signal Bot ✅
This bot supports all Binance coins.

Send your coin like the example below and wait:
/signal BTCUSDT 4h

Note: Signals are based on volume, support/resistance, EMA200, and other indicators.
"""
    await update.message.reply_text(welcome_message)


# دستور /signal
async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.split()
    if len(user_input) < 3:
        await update.message.reply_text("لطفا مانند مثال /signal BTCUSDT 4h وارد کنید.")
        return

    symbol = user_input[1].upper()
    timeframe = user_input[2].lower()

    df = await fetch_ohlcv(symbol=symbol, interval=timeframe)  # اینجا await اضافه شد
    df = add_indicators(df)
    signal_data = generate_signal(df)

    if signal_data is None:
        await update.message.reply_text(
            f"{symbol} | تایم‌فریم: {timeframe}\nسیگنال معتبر برای این ارز و تایم‌فریم موجود نیست."
        )
        return

    message = (
        f"{symbol} | تایم‌فریم: {timeframe}\n"
        f"💰 قیمت فعلی: {signal_data['price']}\n"
        f"🎯 نقطه ورود: {signal_data['entry_price']}\n"
        f"📈 سیگنال: {signal_data['action']}\n"
        f"TP: {signal_data['tp']} | SL: {signal_data['sl']}\n"
        f"💡 سیگنال بر اساس حمایت/مقاومت، EMA200 و حجم ارائه شده."
    )
    await update.message.reply_text(message)


# ساخت اپلیکیشن تلگرام
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.Regex(r"^/signal "), signal))

print("ربات در حال اجراست...")
app.run_polling()
