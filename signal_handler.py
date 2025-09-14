import pandas as pd


def generate_signal(df: pd.DataFrame) -> dict:
    """
    اولویت سیگنال:
    1. حمایت/مقاومت واقعی (بر اساس High/Low کندل‌های اخیر)
    2. EMA200
    3. حجم (برای اعتبار سیگنال)
    """
    if df.empty or len(df) < 20:
        return None

    latest = df.iloc[-1]
    price = latest["close"]
    volume = latest["volume"]
    vol_ma = latest.get("vol_ma", 0)
    ema200 = latest.get("ema200", price)

    # محاسبه حمایت و مقاومت واقعی از 20 کندل اخیر
    lookback = 20
    support = df["low"][-lookback:].min()
    resistance = df["high"][-lookback:].max()

    action = None
    entry_price = price

    # اول: حمایت/مقاومت
    if abs(price - support) / support < 0.05:
        action = "BUY"
        entry_price = support
    elif abs(price - resistance) / resistance < 0.05:
        action = "SELL"
        entry_price = resistance
    else:
        # دوم: EMA200
        action = "BUY" if price > ema200 else "SELL"
        entry_price = price

    # سوم: بررسی حجم برای اعتبار سیگنال
    if volume <= 0:
        return None

    # محاسبه TP و SL
    tp = entry_price * 1.03 if action == "BUY" else entry_price * 0.97
    sl = entry_price * 0.985 if action == "BUY" else entry_price * 1.015

    return {
        "action": action,
        "price": price,
        "entry_price": entry_price,
        "tp": tp,
        "sl": sl,
        "volume": volume,
        "vol_ma": vol_ma,
        "ema200": ema200,
        "support": support,
        "resistance": resistance,
        "timestamp": df.index[-1] if df.index[-1] else None,
    }
