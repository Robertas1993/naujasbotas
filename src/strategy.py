import pandas as pd
from src.indicators import ema, rsi, atr

def generate_signals(df: pd.DataFrame, params: dict = None):
    if params is None:
        params = {"ema_fast": 20, "ema_slow": 50, "rsi_period": 14, "rsi_buy": 40, "rsi_sell": 60, "atr_period": 14, "risk_atr_mult": 3}
    df = df.copy()
    df['ema_fast'] = ema(df['close'], params['ema_fast'])
    df['ema_slow'] = ema(df['close'], params['ema_slow'])
    df['rsi'] = rsi(df['close'], params['rsi_period'])
    df['atr'] = atr(df, params['atr_period'])

    df['signal'] = 0
    long_mask = (df['ema_fast'] > df['ema_slow']) & (df['ema_fast'].shift() <= df['ema_slow'].shift()) & (df['rsi'] < params['rsi_buy'])
    df.loc[long_mask, 'signal'] = 1
    short_mask = (df['ema_fast'] < df['ema_slow']) & (df['ema_fast'].shift() >= df['ema_slow'].shift()) & (df['rsi'] > params['rsi_sell'])
    df.loc[short_mask, 'signal'] = -1

    df['stop_loss'] = df['close'] - params['risk_atr_mult'] * df['atr']
    df['take_profit'] = df['close'] + 2 * params['risk_atr_mult'] * df['atr']
    return df