"""
Technical Indicators Module
Implements various technical analysis indicators for trading signals
"""

import pandas as pd
from typing import List, Tuple


def calculate_rsi(prices: List[float], period: int = 14) -> float:
    """
    Calculate RSI (Relative Strength Index) indicator
    
    Args:
        prices: List of closing prices
        period: RSI period (default: 14)
    
    Returns:
        RSI value (0-100)
    """
    deltas = pd.Series(prices).diff()
    gain = (deltas.where(deltas > 0, 0)).rolling(window=period).mean()
    loss = (-deltas.where(deltas < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return float(rsi.iloc[-1])


def calculate_ema(prices: List[float], period: int) -> float:
    """
    Calculate EMA (Exponential Moving Average) indicator
    
    Args:
        prices: List of closing prices
        period: EMA period
    
    Returns:
        EMA value
    """
    return float(pd.Series(prices).ewm(span=period, adjust=False).mean().iloc[-1])


def calculate_atr(high: List[float], low: List[float], close: List[float], period: int = 14) -> float:
    """
    Calculate ATR (Average True Range) indicator
    
    Args:
        high: List of high prices
        low: List of low prices
        close: List of closing prices
        period: ATR period (default: 14)
    
    Returns:
        ATR value
    """
    df = pd.DataFrame({'high': high, 'low': low, 'close': close})
    df['tr'] = pd.concat([
        df['high'] - df['low'],
        abs(df['high'] - df['close'].shift()),
        abs(df['low'] - df['close'].shift())
    ], axis=1).max(axis=1)
    atr = df['tr'].rolling(window=period).mean().iloc[-1]
    return float(atr)


def calculate_sma(prices: List[float], period: int) -> float:
    """
    Calculate SMA (Simple Moving Average)
    
    Args:
        prices: List of closing prices
        period: SMA period
    
    Returns:
        SMA value
    """
    return float(pd.Series(prices).rolling(window=period).mean().iloc[-1])


def calculate_bollinger_bands(prices: List[float], period: int = 20, std_dev: int = 2) -> Tuple[float, float, float]:
    """
    Calculate Bollinger Bands
    
    Args:
        prices: List of closing prices
        period: Period for bands (default: 20)
        std_dev: Number of standard deviations (default: 2)
    
    Returns:
        Tuple of (upper_band, middle_band, lower_band)
    """
    series = pd.Series(prices)
    sma = series.rolling(window=period).mean()
    std = series.rolling(window=period).std()
    
    middle = sma.iloc[-1]
    upper = middle + (std.iloc[-1] * std_dev)
    lower = middle - (std.iloc[-1] * std_dev)
    
    return float(upper), float(middle), float(lower)


def detect_trend(ema_fast: float, ema_slow: float) -> str:
    """
    Detect trend based on EMA crossover
    
    Args:
        ema_fast: Fast EMA (short-term)
        ema_slow: Slow EMA (long-term)
    
    Returns:
        'bullish', 'bearish', or 'neutral'
    """
    if ema_fast > ema_slow:
        return 'bullish'
    elif ema_fast < ema_slow:
        return 'bearish'
    else:
        return 'neutral'
