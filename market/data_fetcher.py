"""
Market Data Module
Handles fetching and processing real-time market data from Binance
"""

import logging
from typing import Dict, Optional
from binance.client import Client
from indicators import (
    calculate_rsi, calculate_ema, calculate_atr, detect_trend
)
from config.settings import TRADING_CONFIG

logger = logging.getLogger(__name__)


class MarketDataFetcher:
    """Handles market data fetching and technical analysis"""
    
    def __init__(self, binance_client: Client):
        """
        Initialize market data fetcher
        
        Args:
            binance_client: Binance API client instance
        """
        self.client = binance_client
        self.symbol = TRADING_CONFIG['symbol']
        self.timeframe = TRADING_CONFIG['timeframe']
    
    def get_market_data(self) -> Optional[Dict]:
        """
        Fetch real-time market data and calculate technical indicators
        
        Returns:
            Dictionary with market data and indicators, or None on error
        """
        try:
            # Get klines (candlestick data)
            klines = self.client.get_klines(
                symbol=self.symbol,
                interval=self.timeframe,
                limit=100
            )
            
            # Extract OHLCV data
            closes = [float(k[4]) for k in klines]
            highs = [float(k[2]) for k in klines]
            lows = [float(k[3]) for k in klines]
            volumes = [float(k[5]) for k in klines]
            
            current_price = closes[-1]
            
            # Calculate technical indicators
            rsi = calculate_rsi(closes, TRADING_CONFIG['rsi_period'])
            ema_fast = calculate_ema(closes, TRADING_CONFIG['ema_fast'])
            ema_slow = calculate_ema(closes, TRADING_CONFIG['ema_slow'])
            atr = calculate_atr(highs, lows, closes, TRADING_CONFIG['atr_period'])
            
            # Calculate volume metrics
            avg_volume = sum(volumes[-20:]) / 20
            current_volume = volumes[-1]
            volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1.0
            
            # Determine trend
            trend = detect_trend(ema_fast, ema_slow)
            
            market_data = {
                'price': current_price,
                'rsi': rsi,
                'ema_fast': ema_fast,
                'ema_slow': ema_slow,
                'atr': atr,
                'volume': current_volume,
                'avg_volume': avg_volume,
                'volume_ratio': volume_ratio,
                'trend': trend,
                'timestamp': self._get_timestamp(),
                'klines': klines  # Keep raw data for advanced analysis
            }
            
            return market_data
            
        except Exception as e:
            logger.error(f"Error fetching market data: {e}")
            return None
    
    def get_current_price(self) -> Optional[float]:
        """Get current price of the symbol"""
        try:
            ticker = self.client.get_symbol_ticker(symbol=self.symbol)
            return float(ticker['price'])
        except Exception as e:
            logger.error(f"Error fetching current price: {e}")
            return None
    
    @staticmethod
    def _get_timestamp() -> str:
        """Get ISO format timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
