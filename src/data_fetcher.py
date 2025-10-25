import os
import ccxt
import time
import pandas as pd
import requests

VANTAGE_BASE = os.getenv("VANTAGE_BASE_URL", "https://api.vantage.com")
VANTAGE_KEY = os.getenv("VANTAGE_API_KEY")
VANTAGE_SECRET = os.getenv("VANTAGE_API_SECRET")

exchange = ccxt.binance({
    'enableRateLimit': True,
})

def fetch_crypto_ohlcv(symbol: str, timeframe: str = "1h", limit: int = 500):
    since = None
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, since=since, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp','open','high','low','close','volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    return df

def fetch_vantage_ohlcv(symbol: str, timeframe: str = "1h", limit: int = 500):
    url = f"{VANTAGE_BASE}/marketdata/ohlc"
    params = {"symbol": symbol.replace("/",""), "period": timeframe.upper(), "limit": limit}
    headers = {"Authorization": f"Bearer {VANTAGE_KEY}"} if VANTAGE_KEY else {}
    r = requests.get(url, params=params, headers=headers, timeout=10)
    r.raise_for_status()
    data = r.json()
    rows = []
    for item in data.get("candles", []):
        rows.append(item)
    if not rows:
        return pd.DataFrame(columns=['open','high','low','close','volume'])
    df = pd.DataFrame(rows, columns=['timestamp','open','high','low','close','volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    return df

def fetch_ohlcv(instrument: str, market_type: str, timeframe: str = "1h", limit: int = 500):
    if market_type == "crypto":
        return fetch_crypto_ohlcv(instrument, timeframe, limit)
    elif market_type == "vantage":
        return fetch_vantage_ohlcv(instrument, timeframe, limit)
    else:
        raise ValueError("Unsupported market_type")