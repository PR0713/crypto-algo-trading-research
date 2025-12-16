import pandas as pd


class HeikinAshiTrendStrategy:
    """
    Heikin-Ashi based trend-following strategy using
    short / long SMA crossover on HA close prices.
    """

    def __init__(
        self,
        short_window: int = 60,
        long_window: int = 300,
    ):
        self.short_window = short_window
        self.long_window = long_window

    @staticmethod
    def compute_heikin_ashi(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        df["ha_close"] = (
            df["open"] + df["high"] + df["low"] + df["close"]
        ) / 4

        df["ha_open"] = 0.0
        df.iloc[0, df.columns.get_loc("ha_open")] = df.iloc[0]["open"]

        for i in range(1, len(df)):
            df.iloc[i, df.columns.get_loc("ha_open")] = (
                df.iloc[i - 1]["ha_open"] + df.iloc[i - 1]["ha_close"]
            ) / 2

        df["ha_high"] = df[["high", "ha_open", "ha_close"]].max(axis=1)
        df["ha_low"] = df[["low", "ha_open", "ha_close"]].min(axis=1)

        return df

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        df["short_sma"] = (
            df["ha_close"].rolling(self.short_window).mean()
        )
        df["long_sma"] = (
            df["ha_close"].rolling(self.long_window).mean()
        )

        df["signal"] = 0
        position = 0

        for i in range(1, len(df)):
            if (
                df.iloc[i]["short_sma"] > df.iloc[i]["long_sma"]
                and position != 1
            ):
                df.iloc[i, df.columns.get_loc("signal")] = 1
                position = 1

            elif (
                df.iloc[i]["short_sma"] < df.iloc[i]["long_sma"]
                and position != -1
            ):
                df.iloc[i, df.columns.get_loc("signal")] = -1
                position = -1

        return df

    def run(self, df: pd.DataFrame) -> pd.DataFrame:
        df = self.compute_heikin_ashi(df)
        df = self.generate_signals(df)
        return df
