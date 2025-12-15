import ccxt
import pandas as pd
from datetime import datetime

exchange = ccxt.binance()

SYMBOLS = ["BTC/USDT", "ETH/USDT"]
TIMEFRAMES = ["1d", "4h"]
START_DATE = "2020-01-01T00:00:00Z"


def fetch_ohlcv(symbol, timeframe):
    since = exchange.parse8601(START_DATE)
    all_data = []

    while True:
        data = exchange.fetch_ohlcv(symbol, timeframe, since=since, limit=1000)
        if not data:
            break

        since = data[-1][0] + 1
        all_data.extend(data)

        if len(data) < 1000:
            break

    df = pd.DataFrame(
        all_data,
        columns=["timestamp", "open", "high", "low", "close", "volume"]
    )
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df


if __name__ == "__main__":
    for symbol in SYMBOLS:
        for tf in TIMEFRAMES:
            df = fetch_ohlcv(symbol, tf)
            fname = symbol.replace("/", "_").lower()
            df.to_csv(f"raw/{fname}_{tf}.csv", index=False)
            print(f"Saved {fname}_{tf}.csv")
