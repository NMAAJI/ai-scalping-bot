"""
Configuration Settings for AI Trading Bot
All sensitive keys should be loaded from environment variables
"""

import os
from typing import Dict

# ============ API KEYS ============
# Load from environment variables for security
BINANCE_API_KEY = os.getenv('BINANCE_API_KEY', 'YOUR_BINANCE_TESTNET_API_KEY')
BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET', 'YOUR_BINANCE_TESTNET_SECRET_KEY')

# Primary AI API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyA1W-qzVyR_hC_Nj-RkvTsVzfh0hDRZyVA')

# Backup AI APIs (for fallback support)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')
TOGETHER_API_KEY = os.getenv('TOGETHER_API_KEY', '')

# Enable autonomous trading (NO human intervention)
AUTONOMOUS_MODE = os.getenv('AUTONOMOUS_MODE', 'true').lower() == 'true'
ENABLE_BACKUP_APIS = os.getenv('ENABLE_BACKUP_APIS', 'true').lower() == 'true'

# ============ BINANCE CONFIGURATION ============
BINANCE_TESTNET_URL = 'https://testnet.binance.vision'
BINANCE_USE_TESTNET = True

# ============ TRADING CONFIGURATION ============
TRADING_CONFIG: Dict = {
    # Trading pair and timeframe
    'symbol': 'BTCUSDT',
    'timeframe': '1m',  # 1 minute candles
    
    # Risk management
    'risk_per_trade': 0.02,  # 2% of account per trade
    'max_positions': 3,
    'min_confidence': 0.7,
    
    # Check intervals
    'check_interval': 60,  # Check every 60 seconds
    
    # ============ TECHNICAL INDICATOR SETTINGS ============
    
    # RSI (Relative Strength Index)
    'rsi_period': 14,
    'rsi_overbought': 70,
    'rsi_oversold': 30,
    
    # EMA (Exponential Moving Average)
    'ema_fast': 9,
    'ema_slow': 21,
    
    # ATR (Average True Range)
    'atr_period': 14,
    'atr_multiplier': 1.5,
    
    # Volume
    'volume_threshold': 1.2,
}

# ============ LOGGING CONFIGURATION ============
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# ============ WEB SERVER CONFIGURATION ============
FLASK_HOST = '0.0.0.0'
FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

# ============ AI MODEL CONFIGURATION ============
AI_MODEL = 'gemini-2.0-flash-exp'
AI_MAX_RETRIES = 3
AI_TIMEOUT = 30

# ============ DATA STORAGE ============
TRADES_LOG_FILE = 'logs/trades.json'
DATA_DIR = 'data'
LOGS_DIR = 'logs'

def get_trading_config(key: str, default=None):
    """Get trading configuration value safely"""
    return TRADING_CONFIG.get(key, default)

def validate_api_keys() -> bool:
    """Validate that required API keys are configured"""
    if not BINANCE_API_KEY or BINANCE_API_KEY == 'YOUR_BINANCE_TESTNET_API_KEY':
        return False
    if not BINANCE_API_SECRET or BINANCE_API_SECRET == 'YOUR_BINANCE_TESTNET_SECRET_KEY':
        return False
    if not GEMINI_API_KEY or GEMINI_API_KEY.startswith('YOUR_'):
        return False
    return True
