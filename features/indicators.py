import numpy as np
import pandas as pd


# ---------------------------------------
# RETURNS
# ---------------------------------------
def returns(series):
    """Simple percentage returns"""
    return series.pct_change()


def log_returns(series):
    """Log returns (continuous compounding form)"""
    return np.log(series).diff()


# ---------------------------------------
# MOVING AVERAGES
# ---------------------------------------

def sma(series, window):
    """Simple Moving Average"""
    return series.rolling(window).mean()


def ema(series, window):
    """Exponential Moving Average"""
    return series.ewm(span=window, adjust=False).mean()

def sma_ratio(series, window=20):
    """simple moving average ratio, x/sma(x)"""
    return series / sma(series, window)

# ---------------------------------------
# RSI (momentum oscillator)
# ---------------------------------------

def rsi(series, period=14):
    """Relative Strength Index"""

    delta = series.diff()

    gain = delta.where(delta > 0, 0).rolling(period).mean()
    loss = -delta.where(delta < 0, 0).rolling(period).mean()

    rs = gain / loss
    return 100 - (100 / (1 + rs))


# ---------------------------------------
# VOLATILITY
# ---------------------------------------

def volatility(series, window=20):
    """Rolling standard deviation of returns"""
    return returns(series).rolling(window).std()


# ---------------------------------------
# BOLLINGER BANDS
# ---------------------------------------

def bollinger_upper(series, window=20, num_std=2):
    """Volatility Bands upper"""
    sma_ = sma(series, window)
    std = series.rolling(window).std()
    return sma_ + num_std * std


def bollinger_lower(series, window=20, num_std=2):
    """"Volatility Bands lower"""
    sma_ = sma(series, window)
    std = series.rolling(window).std()
    return sma_ - num_std * std


# ---------------------------------------
# MOMENTUM
# ---------------------------------------

def momentum(series, window=10):
    """Price momentum over n periods"""
    return series / series.shift(window) - 1





