import pandas as pd


def compute_indicators(
    df,
    ema_trend_window=20,
    rsi_window=14,
    macd_fast=24,
    macd_slow=52,
    macd_signal=18,
):
    """
    Compute EMA trend filter, RSI, and MACD indicators.
    """
    df = df.copy()

    # EMA trend filter
    df["ema_20"] = df["close"].ewm(
        span=ema_trend_window, adjust=False
    ).mean()

    # RSI
    delta = df["close"].diff()
    gain = delta.clip(lower=0).rolling(rsi_window).mean()
    loss = -delta.clip(upper=0).rolling(rsi_window).mean()
    rs = gain / loss
    df["rsi"] = 100 - (100 / (1 + rs))

    # MACD
    ema_fast = df["close"].ewm(span=macd_fast, adjust=False).mean()
    ema_slow = df["close"].ewm(span=macd_slow, adjust=False).mean()
    df["macd"] = ema_fast - ema_slow
    df["signal_line"] = df["macd"].ewm(
        span=macd_signal, adjust=False
    ).mean()

    return df


def generate_signals(
    df,
    rsi_lower=30,
    rsi_upper=70,
):
    """
    Generate MACD + RSI trading signals with EMA trend filter.
    """
    df = df.copy()
    df["signal"] = 0

    sell_condition = (
        (df["rsi"] < rsi_lower)
        & (df["macd"] > df["signal_line"])
        & (df["close"] > df["ema_20"])
    )

    buy_condition = (
        (df["rsi"] > rsi_upper)
        & (df["macd"] < df["signal_line"])
        & (df["close"] < df["ema_20"])
    )

    df.loc[sell_condition, "signal"] = -1
    df.loc[buy_condition, "signal"] = 1

    return df


def deduplicate_signals(df):
    """
    Remove consecutive duplicate signals.
    """
    df = df.copy()

    final_signal = []
    prev = 0

    for s in df["signal"]:
        if s == prev:
            final_signal.append(0)
        else:
            final_signal.append(s)
        prev = s

    df["signal"] = final_signal
    return df
