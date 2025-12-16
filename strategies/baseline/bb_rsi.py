import pandas as pd


def compute_indicators(
    df,
    bb_window=20,
    rsi_window=14,
    bb_k=2,
):
    """
    Compute Bollinger Bands and RSI indicators.
    """
    df = df.copy()

    # Bollinger Bands
    df["sma"] = df["close"].rolling(bb_window).mean()
    std = df["close"].rolling(bb_window).std()
    df["upper_band"] = df["sma"] + bb_k * std
    df["lower_band"] = df["sma"] - bb_k * std

    # RSI
    delta = df["close"].diff()
    gain = delta.clip(lower=0).rolling(rsi_window).mean()
    loss = -delta.clip(upper=0).rolling(rsi_window).mean()
    rs = gain / loss
    df["rsi"] = 100 - (100 / (1 + rs))

    return df


def generate_signals(
    df,
    rsi_lower=30,
    rsi_upper=70,
):
    """
    Generate BB + RSI trading signals.
    """
    df = df.copy()
    df["signal"] = 0

    sell_condition = (
        (df["rsi"] < rsi_lower)
        | (df["close"] < df["lower_band"])
    )

    buy_condition = (
        (df["rsi"] > rsi_upper)
        | (df["close"] > df["upper_band"])
    )

    df.loc[sell_condition, "signal"] = -1
    df.loc[buy_condition, "signal"] = 1

    return df


def deduplicate_signals(df):
    """
    Remove consecutive duplicate signals and
    preserve execution intent.
    """
    df = df.copy()

    final_signal = []
    prev = 0
    last_exec = 0

    for s in df["signal"]:
        if s == prev:
            final_signal.append(0)
        else:
            final_signal.append(s)
            last_exec = s
        prev = s

    df["signal"] = final_signal
    return df
