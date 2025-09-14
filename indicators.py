import pandas as pd
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator
from ta.trend import MACD


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["ema100"] = EMAIndicator(close=out["close"], window=100).ema_indicator()
    out["ema200"] = EMAIndicator(close=out["close"], window=200).ema_indicator()
    out["rsi"] = RSIIndicator(close=out["close"], window=14).rsi()
    macd_obj = MACD(close=out["close"], window_slow=26, window_fast=12, window_sign=9)
    out["macd"] = macd_obj.macd()
    out["macd_signal"] = macd_obj.macd_signal()
    return out.dropna().reset_index(drop=True)
