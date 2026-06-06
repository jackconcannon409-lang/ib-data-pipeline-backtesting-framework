import pandas as pd

from features.indicators import sma, bollinger_upper
from strategies.rules import uptrend_filter


def add_buy_sell_signals(
    df: pd.DataFrame,
    price: pd.Series,
    fast_window: int = 20,
    slow_window: int = 50
):
    """
    Strategy:

    BUY:
        sma_fast>sma_slow

    SELL:
        price > bollinger_upper
        OR sma_fast < sma_slow
    """


    # -----------------------
    # INDICATORS
    # -----------------------
    sma_fast = sma(price, fast_window)
    sma_slow = sma(price, slow_window)
    bb_upper = bollinger_upper(price, fast_window, num_std=2)

    trend = uptrend_filter(sma_fast, sma_slow)

    # -----------------------
    # BUY SIGNAL
    # -----------------------
    df["buy_signal"] = (
        trend==1
    ).astype(int)

    # -----------------------
    # SELL SIGNAL
    # -----------------------
    df["sell_signal"] = (
        (price > bb_upper) | (sma_fast < sma_slow)
    ).astype(int)

    return df








