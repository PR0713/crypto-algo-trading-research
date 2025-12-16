import numpy as np
import pandas as pd


def compute_parabolic_sar(
    df,
    af_start=0.02,
    af_step=0.02,
    af_max=0.2,
):
    """
    Compute Parabolic SAR values.
    """
    df = df.copy()
    sar = [np.nan] * len(df)

    long_position = False
    af = af_start
    ep = df["high"].iloc[0]

    sar[1] = df["low"].iloc[0]

    for i in range(2, len(df)):
        if long_position:
            new_sar = sar[i - 1] + af * (ep - sar[i - 1])
            if df["low"].iloc[i] < new_sar:
                long_position = False
                sar[i] = ep
                af = af_start
                ep = df["low"].iloc[i]
            else:
                sar[i] = new_sar
                if df["high"].iloc[i] > ep:
                    ep = df["high"].iloc[i]
                    af = min(af + af_step, af_max)
        else:
            new_sar = sar[i - 1] - af * (sar[i - 1] - ep)
            if df["high"].iloc[i] > new_sar:
                long_position = True
                sar[i] = ep
                af = af_start
                ep = df["high"].iloc[i]
            else:
                sar[i] = new_sar
                if df["low"].iloc[i] < ep:
                    ep = df["low"].iloc[i]
                    af = min(af + af_step, af_max)

    df["sar"] = sar
    return df


def generate_signals(df):
    """
    Generate buy/sell signals based on SAR crossover.
    """
    df = df.copy()
    df["signal"] = 0

    for i in range(1, len(df) - 1):
        if df["sar"].iloc[i] < df["close"].iloc[i] and df["sar"].iloc[i - 1] > df["close"].iloc[i - 1]:
            df.iloc[i + 1, df.columns.get_loc("signal")] = 1
        elif df["sar"].iloc[i] > df["close"].iloc[i] and df["sar"].iloc[i - 1] < df["close"].iloc[i - 1]:
            df.iloc[i + 1, df.columns.get_loc("signal")] = -1

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
