import os
import time
import yaml
import logging
from src.data_fetcher import fetch_ohlcv
from src.strategy import generate_signals

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("executor")

def place_order_vantage(symbol, side, qty, price=None, order_type="market", test=True):
    logger.info(f"PLACE ORDER (simulated) {symbol} {side} {qty} @ {price} type={order_type} test={test}")
    return {"status":"simulated", "order_id": f"sim-{int(time.time())}"}

def run_paper_loop(config):
    instruments = config['instruments']
    tf = config.get('timeframe', '1h')
    while True:
        for instr in instruments.get('crypto', []) + instruments.get('fx', []):
            market_type = "crypto" if instr in instruments.get('crypto', []) else "vantage"
            try:
                df = fetch_ohlcv(instr, market_type, timeframe=tf, limit=200)
                df = generate_signals(df)
                last_signal = df['signal'].iloc[-2]
                if last_signal == 1:
                    place_order_vantage(instr, "buy", qty=0.001, price=None, order_type="market", test=True)
                elif last_signal == -1:
                    place_order_vantage(instr, "sell", qty=0.001, price=None, order_type="market", test=True)
            except Exception as e:
                logger.exception(f"Error processing {instr}: {e}")
        time.sleep(60)

if __name__ == "__main__":
    cfg_path = os.getenv("CONFIG_PATH", "config.yaml")
    if os.path.exists(cfg_path):
        with open(cfg_path) as f:
            config = yaml.safe_load(f)
    else:
        config = {"instruments":{"crypto":["BTC/USDT"],"fx":["EUR/USD","XAU/USD"]},"timeframe":"1h"}
    run_paper_loop(config)