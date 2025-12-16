import pandas as pd


def compute_indicators(
    df,
    bb_window=20,
    atr_window=14,
    bb_k=2,
):
    """
    Compute Bollinger Bands and ATR.
    """
    df = df.copy()

    # Bollinger Bands
    df["sma"] = df["close"].rolling(bb_window).mean()
    std = df["close"].rolling(bb_window).std()
    df["upper_band"] = df["sma"] + bb_k * std
    df["lower_band"] = df["sma"] - bb_k * std

    # ATR
    high_low = df["high"] - df["low"]
    high_close = (df["high"] - df["close"].shift()).abs()
    low_close = (df["low"] - df["close"].shift()).abs()
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    df["atr"] = tr.ewm(span=atr_window, adjust=False).mean()

    return df


def generate_signals(df, atr_multiplier=1.5):
    """
    Generate BB + ATR trading signals.
    """
    df = df.copy()
    df["signal"] = 0

    sell_condition = (
        (df["close"] > df["close"].shift(1) + atr_multiplier * df["atr"])
        | (df["close"] < df["lower_band"])
    )

    buy_condition = (
        (df["close"] < df["close"].shift(1) - atr_multiplier * df["atr"])
        | (df["close"] > df["upper_band"])
    )

    df.loc[sell_condition, "signal"] = -1
    df.loc[buy_condition, "signal"] = 1

    return df


def deduplicate_signals(df):
    """
    Remove consecutive duplicate signals.
    """
    df = df.copy()
    deduped = []
    prev = 0

    for s in df["signal"]:
        if s == prev:
            deduped.append(0)
        else:
            deduped.append(s)
        prev = s

    df["signal"] = deduped
    return df
