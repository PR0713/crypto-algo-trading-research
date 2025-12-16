import pandas as pd
import pandas_ta as ta


class EMAADXStrategy:
    """
    EMA + ADX trend-following strategy with optional stop-loss.

    Strategy logic:
    - Long when EMA_fast > EMA_mid > EMA_slow and ADX > threshold
    - Short when EMA_fast < EMA_mid < EMA_slow and ADX < threshold
    - Optional stop-loss to limit downside
    """

    def __init__(
        self,
        ema_fast: int = 9,
        ema_mid: int = 11,
        ema_slow: int = 45,
        adx_window: int = 14,
        adx_threshold: float = 15.0,
        stop_loss_pct: float = 0.05,
    ):
        self.ema_fast = ema_fast
        self.ema_mid = ema_mid
        self.ema_slow = ema_slow
        self.adx_window = adx_window
        self.adx_threshold = adx_threshold
        self.stop_loss_pct = stop_loss_pct

    def compute_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        df["ema_fast"] = ta.ema(df["close"], length=self.ema_fast)
        df["ema_mid"] = ta.ema(df["close"], length=self.ema_mid)
        df["ema_slow"] = ta.ema(df["close"], length=self.ema_slow)

        adx = ta.adx(
            df["high"],
            df["low"],
            df["close"],
            length=self.adx_window,
        )
        df["adx"] = adx[f"ADX_{self.adx_window}"]

        return df

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generates discrete trading signals:
        -  1 : Enter / hold long
        - -1 : Enter / hold short
        -  0 : No action
        """
        df = df.copy()
        df["signal"] = 0

        position = 0
        entry_price = None

        for i in range(1, len(df)):
            price = df.iloc[i]["close"]

            long_condition = (
                df.iloc[i]["ema_fast"] > df.iloc[i]["ema_mid"]
                and df.iloc[i]["ema_mid"] > df.iloc[i]["ema_slow"]
                and df.iloc[i]["adx"] > self.adx_threshold
            )

            short_condition = (
                df.iloc[i]["ema_fast"] < df.iloc[i]["ema_mid"]
                and df.iloc[i]["ema_mid"] < df.iloc[i]["ema_slow"]
                and df.iloc[i]["adx"] < self.adx_threshold
            )

            # Enter long
            if long_condition and position != 1:
                df.iloc[i, df.columns.get_loc("signal")] = 1
                position = 1
                entry_price = price

            # Enter short
            elif short_condition and position != -1:
                df.iloc[i, df.columns.get_loc("signal")] = -1
                position = -1
                entry_price = price

            # Stop-loss for long
            if (
                position == 1
                and entry_price is not None
                and price <= entry_price * (1 - self.stop_loss_pct)
            ):
                df.iloc[i, df.columns.get_loc("signal")] = -1
                position = 0
                entry_price = None

        return df
