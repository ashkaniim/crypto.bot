import httpx
import pandas as pd
from datetime import datetime
from config import CACHE_TTL

BINANCE_URL = "https://api.binance.com/api/v3/klines"

cache = {}


async def fetch_ohlcv(
    symbol: str = "BTCUSDT", interval: str = "1h", limit: int = 1000
) -> pd.DataFrame:
    key = f"{symbol}_{interval}"
    now = datetime.utcnow()

    if key in cache:
        cached_data, timestamp = cache[key]
        if (now - timestamp).seconds < CACHE_TTL:
            return cached_data

    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(
            BINANCE_URL,
            params={"symbol": symbol.upper(), "interval": interval, "limit": limit},
        )
        r.raise_for_status()
        raw = r.json()

    df = pd.DataFrame(
        raw,
        columns=[
            "open_time",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "close_time",
            "qav",
            "num_trades",
            "taker_base",
            "taker_quote",
            "ignore",
        ],
    )
    for col in ["open", "high", "low", "close", "volume"]:
        df[col] = df[col].astype(float)
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms", utc=True)
    df["close_time"] = pd.to_datetime(df["close_time"], unit="ms", utc=True)
    df["vol_ma"] = df["volume"].rolling(window=20).mean()
    df = df[
        ["open_time", "open", "high", "low", "close", "volume", "close_time", "vol_ma"]
    ]

    cache[key] = (df, now)
    return df
