from features.indicators import sma


def uptrend_filter(short_series="sma20", long_series="sma50", shift=1):
    """
    Only allow trades in uptrend
    """

    signal = short_series > long_series
    return signal.shift(shift)


