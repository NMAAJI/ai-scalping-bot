"""
Utility functions for the trading bot
"""

import json
import logging
import os
from typing import Dict, List
from datetime import datetime

logger = logging.getLogger(__name__)


def setup_logging(log_level: str = 'INFO', log_format: str = None) -> None:
    """
    Configure logging for the application
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format: Log message format string
    """
    if log_format is None:
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper(), logging.INFO),
        format=log_format
    )


def ensure_directories_exist(directories: List[str]) -> None:
    """
    Ensure required directories exist
    
    Args:
        directories: List of directory paths to create
    """
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.info(f"Directory ensured: {directory}")


def save_trades_to_file(trades: List[Dict], filepath: str) -> bool:
    """
    Save trades to JSON file
    
    Args:
        trades: List of trade dictionaries
        filepath: Path to save JSON file
    
    Returns:
        True if successful, False otherwise
    """
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(trades, f, indent=2, default=str)
        logger.info(f"Trades saved to {filepath}")
        return True
    except Exception as e:
        logger.error(f"Error saving trades: {e}")
        return False


def load_trades_from_file(filepath: str) -> List[Dict]:
    """
    Load trades from JSON file
    
    Args:
        filepath: Path to JSON file
    
    Returns:
        List of trade dictionaries, or empty list if file doesn't exist
    """
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"Error loading trades: {e}")
    return []


def format_currency(value: float, decimals: int = 2) -> str:
    """
    Format value as currency string
    
    Args:
        value: Numeric value
        decimals: Number of decimal places
    
    Returns:
        Formatted currency string
    """
    return f"${value:,.{decimals}f}"


def format_percentage(value: float, decimals: int = 2) -> str:
    """
    Format value as percentage string
    
    Args:
        value: Numeric value (as decimal, e.g., 0.05 for 5%)
        decimals: Number of decimal places
    
    Returns:
        Formatted percentage string
    """
    return f"{value * 100:.{decimals}f}%"


def get_timestamp() -> str:
    """Get ISO format timestamp"""
    return datetime.now().isoformat()


def calculate_risk_reward_ratio(entry: float, stop_loss: float, take_profit: float) -> float:
    """
    Calculate risk-reward ratio for a trade
    
    Args:
        entry: Entry price
        stop_loss: Stop loss price
        take_profit: Take profit price
    
    Returns:
        Risk-reward ratio
    """
    risk = abs(entry - stop_loss)
    reward = abs(take_profit - entry)
    
    if risk == 0:
        return 0
    
    return reward / risk


def validate_trading_pair(symbol: str) -> bool:
    """
    Validate trading pair format
    
    Args:
        symbol: Trading pair symbol (e.g., 'BTCUSDT')
    
    Returns:
        True if valid, False otherwise
    """
    return isinstance(symbol, str) and len(symbol) >= 6


class RateLimiter:
    """Simple rate limiter for API calls"""
    
    def __init__(self, max_calls: int, time_window: int):
        """
        Initialize rate limiter
        
        Args:
            max_calls: Maximum number of calls allowed
            time_window: Time window in seconds
        """
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = []
    
    def is_allowed(self) -> bool:
        """
        Check if a call is allowed
        
        Returns:
            True if call is allowed, False if rate limit exceeded
        """
        from datetime import datetime, timedelta
        
        now = datetime.now()
        cutoff = now - timedelta(seconds=self.time_window)
        
        # Remove old calls outside time window
        self.calls = [call for call in self.calls if call > cutoff]
        
        if len(self.calls) < self.max_calls:
            self.calls.append(now)
            return True
        
        return False
