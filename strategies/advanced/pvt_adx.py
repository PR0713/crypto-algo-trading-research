import pandas as pd
import pandas_ta as ta


class PVTADXStrategy:
    """
    Price Volume Trend (PVT) + ADX trend-following strategy.

    Logic:
    - Long when PVT > EMA and ADX > threshold
    - Short when PVT < EMA and ADX < threshold
    """

    def __init__(
        self,
        ema_length: int = 200,
        adx_length: int = 14,
        adx_threshold: float = 15.0,
    ):
        self.ema_length = ema_length
        self.adx_length = adx_length
        self.adx_threshold = adx_threshold

    def compute_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        # EMA on price
        df["ema"] = ta.ema(df["close"], length=self.ema_length)

        # Price Volume Trend (PVT)
        pvt = ((df["close"] - df["close"].shift(1)) / df["close"].shift(1)) * df["volume"]
        df["pvt"] = pvt.cumsum()

        # ADX
        adx = ta.adx(
            df["high"],
            df["low"],
            df["close"],
            length=self.adx_length,
        )
        df["adx"] = adx[f"ADX_{self.adx_length}"]

        return df

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df["signal"] = 0

        position = 0

        for i in range(1, len(df)):
            long_condition = (
                df.iloc[i]["pvt"] > df.iloc[i]["ema"]
                and df.iloc[i]["adx"] > self.adx_threshold
            )

            short_condition = (
                df.iloc[i]["pvt"] < df.iloc[i]["ema"]
                and df.iloc[i]["adx"] < self.adx_threshold
            )

            if long_condition and position != 1:
                df.iloc[i, df.columns.get_loc("signal")] = 1
                position = 1

            elif short_condition and position != -1:
                df.iloc[i, df.columns.get_loc("signal")] = -1
                position = -1

        return df
