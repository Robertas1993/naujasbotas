import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import pandas as pd
import numpy as np
from src.backtest import simple_backtest

# Sugeneruojami sintetiniai OHLCV duomenys
np.random.seed(42)
length = 300
dates = pd.date_range(end=pd.Timestamp.utcnow(), periods=length, freq='H')
prices = 1000 + np.cumsum(np.random.normal(0, 1, size=length))
openp = prices
closep = prices + np.random.normal(0, 0.5, size=length)
highp = np.maximum(openp, closep) + np.abs(np.random.normal(0, 0.5, size=length))
lowp = np.minimum(openp, closep) - np.abs(np.random.normal(0, 0.5, size=length))
vol = np.random.randint(1, 100, size=length)

df = pd.DataFrame({
    'open': openp,
    'high': highp,
    'low': lowp,
    'close': closep,
    'volume': vol
}, index=dates)

config = {
    "backtest": {
        "commission_pct": 0.05,
        "slippage_pct": 0.05
    },
    "risk": {
        "risk_per_trade_pct": 1.0
    },
    "initial_capital": 10000.0
}

result = simple_backtest(df, config)
print("Demo backtest result:")
print(result)