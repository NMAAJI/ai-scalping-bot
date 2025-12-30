# 🤖 AI SCALPING BOT - COMPLETE DETAILED DOCUMENTATION

**Status**: ✅ Production Ready | **Date**: December 2025  
**License**: Free & Open Source | **Python**: 3.10+ | **Node.js**: 14+

---

## 📋 TABLE OF CONTENTS

1. [Project Overview](#project-overview)
2. [Architecture & Structure](#architecture--structure)
3. [Features in Detail](#features-in-detail)
4. [Installation Guide](#installation-guide)
5. [Configuration](#configuration)
6. [Running the Bot](#running-the-bot)
7. [Backend Components](#backend-components)
8. [Frontend Components](#frontend-components)
9. [API Endpoints](#api-endpoints)
10. [Trading Logic](#trading-logic)
11. [AI Integration](#ai-integration)
12. [Risk Management](#risk-management)
13. [Database Structure](#database-structure)
14. [Troubleshooting](#troubleshooting)

---

## PROJECT OVERVIEW

### What is This Project?

The **AI Scalping Bot** is a fully automated cryptocurrency trading bot that:
- **Trades on Binance Testnet** (safe, no real money)
- **Uses Google Gemini AI** to make buy/sell decisions
- **Has Backup AI Services** (OpenAI, Anthropic) for failover
- **Runs in Autonomous Mode** (no human approval needed)
- **Provides a React Dashboard** for real-time monitoring
- **Stores Trade History** in SQLite database
- **Manages Risk** with stop-losses and position limits

### Key Statistics

| Metric | Value |
|--------|-------|
| **Trading Pair** | BTCUSDT (Bitcoin) |
| **Timeframe** | 1-minute candles |
| **Check Interval** | 60 seconds |
| **Max Positions** | 3 simultaneous trades |
| **Risk Per Trade** | 2% of account |
| **Min Confidence** | 70% |
| **API** | Binance Testnet (no real money) |
| **AI Model** | Gemini 2.0 Flash |

### Technology Stack

**Backend:**
- Python 3.10+
- Flask (Web server)
- Binance Python Client
- Google Gemini API
- SQLite (Database)
- Pandas, NumPy (Data analysis)

**Frontend:**
- React 18
- Modern JavaScript (ES6+)
- CSS3 with dark theme
- Real-time polling (3-second intervals)
- Responsive design (mobile-friendly)

---

## ARCHITECTURE & STRUCTURE

### Complete Directory Tree

```
ai-scalping-bot/
│
├── 📄 MAIN ENTRY FILES
│   ├── main.py                    # Primary entry point (Flask + Bot)
│   ├── bot.py                     # Alternative bot implementation
│   └── start.py                   # Startup script
│
├── 📁 ai/                         # AI & Autonomous Trading
│   ├── __init__.py
│   ├── analyzer.py                # Gemini AI analysis
│   ├── autonomous_engine.py       # Fully autonomous trading
│   ├── autonomous_trader.py       # Autonomous execution
│   └── backup_services.py         # OpenAI, Anthropic fallback
│
├── 📁 trading/                    # Trade Execution
│   ├── __init__.py
│   ├── executor.py                # Place orders, manage positions
│   └── auto_engine.py             # Automated trading engine
│
├── 📁 market/                     # Market Data
│   ├── __init__.py
│   └── data_fetcher.py            # Fetch prices, indicators
│
├── 📁 indicators/                 # Technical Indicators
│   ├── __init__.py                # RSI, EMA, ATR, Volume, Trend
│
├── 📁 config/                     # Configuration
│   ├── __init__.py
│   └── settings.py                # All config (API keys, params)
│
├── 📁 utils/                      # Utilities
│   ├── __init__.py
│   ├── database.py                # SQLite management
│   ├── helpers.py                 # Logging, validation
│
├── 📁 web/                        # Flask Web Server
│   ├── __init__.py
│   ├── react_dashboard.py         # Flask routes
│   ├── static/                    # Built React files
│   │   ├── index.html
│   │   ├── js/
│   │   └── css/
│   └── templates/                 # HTML templates
│
├── 📁 frontend/                   # React Frontend (Source)
│   ├── package.json
│   ├── build.bat / build.sh       # Build scripts
│   ├── public/
│   │   └── index.html
│   └── src/
│       ├── index.jsx              # React entry
│       ├── App.jsx                # Main React component
│       ├── components/
│       │   ├── Dashboard.jsx      # Main dashboard container
│       │   ├── Overview.jsx       # Status & metrics
│       │   ├── Chart.jsx          # Price chart
│       │   ├── Analytics.jsx      # Trade analytics
│       │   ├── Journal.jsx        # Trade journal
│       │   └── Performance.jsx    # Performance metrics
│       ├── utils/
│       │   ├── api.js             # API client
│       │   ├── constants.js       # Constants
│       │   └── helpers.js         # Helper functions
│       └── styles/
│           ├── dashboard.css      # Dashboard styles
│           ├── globals.css        # Global styles
│           └── tables.css         # Table styles
│
├── 📁 data/                       # Trade data storage
│
├── 📁 logs/                       # Log files
│
├── 📄 requirements.txt            # Python dependencies
├── 📄 .env                        # Environment variables (DO NOT COMMIT)
├── 📄 README.md                   # Quick start
└── 📄 README_DETAILED.md          # This file

```

---

## FEATURES IN DETAIL

### 1. Autonomous Trading System

**What it does:**
- Monitors market 24/7 every 60 seconds
- Analyzes price, RSI, EMA, volume, trend
- Sends market data to Gemini AI
- Receives BUY/SELL/HOLD decision
- Automatically executes trades (no approval needed)
- Tracks all trades in database

**Key Files:**
- [ai/autonomous_engine.py](ai/autonomous_engine.py)
- [ai/autonomous_trader.py](ai/autonomous_trader.py)
- [trading/executor.py](trading/executor.py)

### 2. AI Decision Making

**Gemini AI Analyzes:**
- **Price Action**: Current price, trend direction
- **RSI**: Overbought (>70) / Oversold (<30)
- **Moving Averages**: Fast EMA (9) vs Slow EMA (21)
- **Volume**: Current vs average volume
- **ATR**: Volatility for stop-loss sizing

**AI Decision Output:**
```json
{
  "action": "BUY",                    // BUY, SELL, or HOLD
  "confidence": 0.85,                 // 0.0 to 1.0 (85%)
  "entry_price": 42500.50,            // Where to buy
  "stop_loss": 42100.00,              // Where to exit if wrong
  "take_profit": 43500.00,            // Where to exit if right
  "reasoning": "Bullish crossover..."
}
```

**Key Files:**
- [ai/analyzer.py](ai/analyzer.py) - Gemini API integration
- [config/settings.py](config/settings.py) - AI prompt configuration

### 3. Real-Time Dashboard

**6 Tabs:**

| Tab | Purpose | Data Shown |
|-----|---------|-----------|
| **Overview** | Quick status | Bot running, balance, trades today, win rate, current price |
| **Chart** | Price visualization | Price chart, RSI, MACD, volume, trend indicators |
| **Analytics** | Trade analysis | Win/loss pie chart, daily stats, performance trends |
| **Journal** | Trade history | All trades with entry/exit, P&L, timestamps |
| **Performance** | Risk metrics | Sharpe ratio, max drawdown, ROI, monthly breakdown |

**Key Files:**
- [frontend/src/components/Dashboard.jsx](frontend/src/components/Dashboard.jsx)
- [frontend/src/utils/api.js](frontend/src/utils/api.js)

### 4. Risk Management

**Position Sizing:**
- Max 3 positions open simultaneously
- Each trade risks only 2% of account
- Quantity = (Account * Risk%) / (Entry - Stop Loss)

**Stop Loss & Take Profit:**
- Stop Loss = Entry - (ATR × 1.5)
- Take Profit = Entry + (ATR × 1.5)

**Confidence Filter:**
- Only executes trades with ≥70% confidence
- Skips low-confidence signals

**Key Files:**
- [trading/executor.py](trading/executor.py#L50-L100)

### 5. Backup AI Services

**If Gemini Fails:**
1. Try OpenAI GPT (if key available)
2. Try Anthropic Claude (if key available)
3. Use fallback HOLD decision

**Key Files:**
- [ai/backup_services.py](ai/backup_services.py)

---

## INSTALLATION GUIDE

### Step 1: Prerequisites

**What you need:**
- Windows, Mac, or Linux computer
- Python 3.10 or higher
- Node.js 14 or higher
- Git (optional)
- Internet connection

**Check your versions:**
```powershell
# Windows PowerShell
python --version
node --version
npm --version
```

### Step 2: Get Binance Testnet Keys

1. Go to: https://testnet.binance.vision/
2. Click "Login" (create account if needed)
3. Go to "API Management"
4. Create new key (name: "AI Bot")
5. Copy: API Key and Secret Key
6. Enable: "Spot Trading" (leave others off)
7. Whitelist your IP (optional, but recommended)

### Step 3: Get Google Gemini API Key

1. Go to: https://ai.google.dev/
2. Click "Get API Key"
3. Click "Create API key"
4. Copy the key

### Step 4: Clone & Setup Project

```powershell
# Navigate to project folder
cd c:\Users\Maajid\ai-scalping-bot

# Create Python virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\Activate.ps1

# Install Python dependencies
pip install -r requirements.txt

# Go to frontend folder
cd frontend

# Install React dependencies
npm install

# Go back to root
cd ..
```

### Step 5: Build React Frontend

```powershell
# Windows
frontend\build.bat

# Mac/Linux
bash frontend/build.sh
```

This creates the built files in `web/static/`

### Step 6: Configure Environment Variables

Create `.env` file in root directory:

```env
# Binance API Keys (from testnet)
BINANCE_API_KEY=your_testnet_api_key_here
BINANCE_API_SECRET=your_testnet_secret_here

# Gemini AI API Key
GEMINI_API_KEY=your_gemini_api_key_here

# Backup AI APIs (optional)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Trading Settings
AUTONOMOUS_MODE=true
ENABLE_BACKUP_APIS=true
LOG_LEVEL=INFO
FLASK_PORT=5000
FLASK_DEBUG=False
```

**⚠️ NEVER commit `.env` to Git! It contains secrets!**

---

## CONFIGURATION

### Trading Config (config/settings.py)

```python
TRADING_CONFIG = {
    # What to trade
    'symbol': 'BTCUSDT',           # Bitcoin (only)
    'timeframe': '1m',              # 1-minute candles
    
    # Risk management
    'risk_per_trade': 0.02,         # 2% of account per trade
    'max_positions': 3,             # Never more than 3 open trades
    'min_confidence': 0.7,          # 70% minimum AI confidence
    'check_interval': 60,           # Check every 60 seconds
    
    # RSI (Relative Strength Index)
    'rsi_period': 14,               # Standard 14-period
    'rsi_overbought': 70,           # >70 = potentially sold out (SELL signal)
    'rsi_oversold': 30,             # <30 = potentially bought out (BUY signal)
    
    # EMA (Exponential Moving Averages)
    'ema_fast': 9,                  # Fast MA for quick reversals
    'ema_slow': 21,                 # Slow MA for trend direction
    
    # ATR (Average True Range)
    'atr_period': 14,               # Standard 14-period
    'atr_multiplier': 1.5,          # Stop/TP distance = ATR × 1.5
    
    # Volume
    'volume_threshold': 1.2,        # Need 1.2x average volume
}
```

### API Configuration

```python
# Primary AI (Gemini)
AI_MODEL = 'gemini-2.0-flash-exp'
AI_MAX_RETRIES = 3                  # Retry 3 times on failure
AI_TIMEOUT = 30                     # 30 second timeout

# Flask Server
FLASK_HOST = '0.0.0.0'              # Listen on all interfaces
FLASK_PORT = 5000                   # http://localhost:5000
FLASK_DEBUG = False                 # Set True only in development

# Logging
LOG_LEVEL = 'INFO'                  # DEBUG, INFO, WARNING, ERROR
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Data Storage
TRADES_LOG_FILE = 'logs/trades.json'
DATA_DIR = 'data'
LOGS_DIR = 'logs'
```

---

## RUNNING THE BOT

### Start the Complete System

```powershell
# From root directory
python main.py
```

**You should see:**
```
========================================================================
🤖 AUTONOMOUS MODE ENABLED - FULLY AUTOMATED AI TRADING
⚠️ NO HUMAN INTERVENTION REQUIRED - DIRECT API DECISION EXECUTION
========================================================================
✅ All services initialized
🚀 Bot starting in autonomous mode...
📊 Dashboard available at: http://localhost:5000
```

### Access the Dashboard

Open your browser:
```
http://localhost:5000
```

You should see:
- 6 tabs at top (Overview, Chart, Analytics, Journal, Performance)
- Real-time data updating every 3 seconds
- Bot status (running/stopped)
- Current trades and balance

### Stop the Bot

Press `Ctrl+C` in the terminal where it's running.

---

## BACKEND COMPONENTS

### 1. main.py - Entry Point

**What it does:**
- Initializes Flask web server
- Sets up all services (Binance, AI, Database)
- Starts the autonomous trading loop
- Serves the React dashboard
- Provides REST API endpoints

**Flow:**
```
main.py
├── Load environment variables (.env)
├── Initialize Flask app
├── Initialize Binance client
├── Initialize Gemini AI
├── Initialize Database
├── Start trading thread (autonomous_engine.py)
├── Start Flask server (port 5000)
└── Listen for API requests
```

**Key Functions:**
- `initialize_services()` - Set up all components
- `run_autonomous_trading()` - Main trading loop
- Flask routes for API endpoints

### 2. ai/analyzer.py - Gemini AI Analysis

**Purpose:** Make trading decisions using AI

**Class: GeminiAnalyzer**

```python
class GeminiAnalyzer:
    def analyze_market(self, market_data: Dict) -> Dict:
        """
        Input: Market data (price, RSI, EMA, volume, etc.)
        Output: Trading decision (action, confidence, entry, stop, TP)
        """
```

**How it works:**
1. Receives market data from `MarketDataFetcher`
2. Builds AI prompt with technical indicators
3. Sends to Gemini API
4. Parses JSON response
5. Returns decision with confidence level

**Prompt Template:**
```
You are an expert scalping trader. Analyze this data:
- Current Price: $42,500
- RSI: 65
- Fast EMA: $42,400
- Slow EMA: $42,200
- Volume Ratio: 1.5x

BUY if: Fast > Slow, RSI < 70, Volume up, bullish trend
SELL if: Fast < Slow, RSI > 30, Volume up, bearish trend
HOLD otherwise

Respond in JSON format...
```

### 3. market/data_fetcher.py - Real-Time Market Data

**Purpose:** Fetch and analyze live market data

**Class: MarketDataFetcher**

```python
class MarketDataFetcher:
    def get_market_data(self) -> Dict:
        """
        Output example:
        {
            'price': 42500.50,
            'rsi': 65.25,
            'ema_fast': 42400.00,
            'ema_slow': 42200.00,
            'atr': 150.00,
            'volume': 125.5,
            'avg_volume': 100.2,
            'volume_ratio': 1.25,
            'trend': 'BULLISH',
            'timestamp': '2025-12-27T10:30:00Z'
        }
        """
```

**Data Sources:**
- **Candles**: Last 100 × 1-minute candles from Binance
- **Close Prices**: Extract closing prices for indicators
- **Volume**: Current vs last 20-candle average

**Indicators Calculated:**
- **RSI (14)**: Momentum oscillator (0-100)
- **EMA (9, 21)**: Trend direction
- **ATR (14)**: Volatility measure
- **Volume Ratio**: Current vol ÷ avg vol
- **Trend**: BULLISH (fast > slow) or BEARISH (fast < slow)

### 4. trading/executor.py - Execute Trades

**Purpose:** Place orders and manage positions

**Class: TradeExecutor**

```python
class TradeExecutor:
    def execute_trade(self, ai_decision: Dict, market_data: Dict) -> Dict:
        """
        Takes AI decision and places order
        Returns execution result
        """
```

**Pre-Execution Checks:**
1. Is position already open? → Skip
2. Is confidence > 70%? → Skip if not
3. Are we at max 3 positions? → Skip if yes
4. Is stop-loss different from entry? → Skip if equal

**Order Placement:**
1. Calculate quantity based on risk (2%)
2. Place MARKET order (BUY or SELL)
3. Store position in `active_positions`
4. Log trade to database

**Position Tracking:**
```python
position = {
    'symbol': 'BTCUSDT',
    'action': 'BUY',
    'entry_price': 42500.50,
    'stop_loss': 42100.00,
    'take_profit': 43500.00,
    'quantity': 0.001,
    'entry_time': '2025-12-27T10:30:00Z',
    'confidence': 0.85,
    'reasoning': 'Bullish EMA crossover with volume'
}
```

**Position Closing:**
- If price hits take profit → Close with PROFIT
- If price hits stop loss → Close with LOSS
- Manual close via dashboard

### 5. ai/autonomous_engine.py - Autonomous Trading Loop

**Purpose:** Run 24/7 trading without human input

**Class: FullyAutonomousTrader**

**Main Loop:**
```
Every 60 seconds:
1. Fetch latest market data
2. Send to Gemini AI for analysis
3. Get trading decision (BUY/SELL/HOLD)
4. If confident enough:
   ├── Check position limits
   ├── Calculate quantity
   └── Execute order
5. Monitor open positions
6. Close positions if SL/TP hit
7. Update database
8. Log to file
```

**Key Methods:**
- `start()` - Begin autonomous trading
- `stop()` - Stop gracefully
- `_trading_loop()` - Main iteration
- `_handle_decision()` - Execute if warranted

### 6. utils/database.py - Trade History

**Purpose:** Store all trades in SQLite database

**Database Schema:**

```sql
-- Trades Table
CREATE TABLE trades (
    id INTEGER PRIMARY KEY,
    symbol TEXT,
    action TEXT,              -- BUY or SELL
    entry_price REAL,
    exit_price REAL,
    quantity REAL,
    entry_time TEXT,
    exit_time TEXT,
    profit_loss REAL,
    profit_loss_percent REAL,
    confidence REAL,
    reasoning TEXT
);

-- Positions Table
CREATE TABLE positions (
    id INTEGER PRIMARY KEY,
    symbol TEXT,
    action TEXT,
    entry_price REAL,
    current_price REAL,
    stop_loss REAL,
    take_profit REAL,
    quantity REAL,
    entry_time TEXT,
    unrealized_pl REAL
);
```

---

## FRONTEND COMPONENTS

### React Architecture

**Framework:** React 18 + JavaScript (ES6+)  
**Build Tool:** Webpack (via build scripts)  
**Styling:** CSS3 with variables  
**API Client:** Custom fetch-based client  

### Component Structure

#### 1. App.jsx - Root Component
- Loads configuration
- Renders main layout
- Handles global state

#### 2. Dashboard.jsx - Container Component
**Purpose:** Manage state and data fetching

**State:**
```javascript
{
  activeTab: 'overview',          // Current tab
  data: {
    bot_running: true,
    balance: 10000,
    trades_today: 5,
    win_rate: 0.65,
    total_pl: 1200.50,
    current_price: 42500
  },
  loading: false,
  error: null,
  lastUpdate: '10:30:45 AM'
}
```

**Data Fetching:**
```javascript
useEffect(() => {
  // Fetch all data
  await Promise.all([
    apiClient.getStatus(),
    apiClient.getAnalytics(),
    apiClient.getTradeHistory(),
    apiClient.getMarketData(),
    apiClient.getPerformanceMetrics()
  ]);
  
  // Poll every 3 seconds
}, []);
```

#### 3. Overview.jsx - Status Dashboard
**Shows:**
- Bot running status (toggle button)
- Account balance
- Trades today
- Win rate percentage
- Total P&L
- Recent trades table

**Table Columns:**
| Time | Symbol | Action | Entry | Exit | P&L | % |
|------|--------|--------|-------|------|-----|---|
| 10:30 | BTCUSDT | BUY | 42500 | 42650 | $150 | +0.35% |

#### 4. Chart.jsx - Price Visualization
**Shows:**
- Price line chart (last 24 hours)
- RSI indicator
- MACD indicator
- Volume bars
- Trend direction

**Chart Library:** Chart.js or Recharts

#### 5. Analytics.jsx - Trade Analysis
**Shows:**
- Win/Loss pie chart
- Daily stats graph
- Performance trends
- Trade distribution

**Metrics:**
- Total trades
- Winning trades
- Losing trades
- Win rate %
- Average win
- Average loss

#### 6. Journal.jsx - Trade Journal
**Shows:** Complete trade history

**Table Columns:**
```
| Entry Time | Symbol | Action | Entry Price | Exit Price | Quantity | P&L | P&L % | Status |
|------------|--------|--------|------------|-----------|----------|-----|-------|--------|
| 10:30 AM | BTCUSDT | BUY | 42500.00 | 42650.50 | 0.001 | $150 | +0.35% | Closed |
```

#### 7. Performance.jsx - Risk Metrics
**Shows:**
- Sharpe Ratio (risk-adjusted returns)
- Maximum Drawdown (worst loss)
- Return on Investment (ROI)
- Monthly P&L breakdown
- Cumulative returns chart

---

## API ENDPOINTS

### Status Endpoints

**GET /api/status**
```json
{
  "bot_running": true,
  "balance": 10000.50,
  "trades_today": 5,
  "win_rate": 0.65,
  "total_pl": 1200.50,
  "current_price": 42500.00,
  "timestamp": "2025-12-27T10:30:00Z"
}
```

**POST /api/toggle-trading**
```json
{
  "status": "success",
  "running": true
}
```

### Market Data Endpoints

**GET /api/market-data**
```json
{
  "symbol": "BTCUSDT",
  "price": 42500.00,
  "rsi": 65.25,
  "ema_fast": 42400.00,
  "ema_slow": 42200.00,
  "atr": 150.00,
  "volume": 125.5,
  "trend": "BULLISH"
}
```

### Trade Endpoints

**GET /api/trades**
```json
{
  "trades": [
    {
      "id": 1,
      "symbol": "BTCUSDT",
      "action": "BUY",
      "entry_price": 42500.00,
      "exit_price": 42650.50,
      "quantity": 0.001,
      "entry_time": "2025-12-27T10:30:00Z",
      "exit_time": "2025-12-27T10:35:00Z",
      "profit_loss": 150.50,
      "profit_loss_percent": 0.35
    }
  ]
}
```

**GET /api/positions**
```json
{
  "positions": [
    {
      "id": 1,
      "symbol": "BTCUSDT",
      "action": "BUY",
      "entry_price": 42500.00,
      "current_price": 42550.00,
      "stop_loss": 42100.00,
      "take_profit": 43500.00,
      "quantity": 0.001,
      "unrealized_pl": 50.00
    }
  ]
}
```

### Analytics Endpoints

**GET /api/analytics**
```json
{
  "total_trades": 150,
  "winning_trades": 97,
  "losing_trades": 53,
  "win_rate": 0.6467,
  "average_win": 125.50,
  "average_loss": -85.25,
  "profit_factor": 2.15,
  "daily_stats": [
    {"date": "2025-12-27", "trades": 5, "pl": 1200.50}
  ]
}
```

**GET /api/performance**
```json
{
  "total_pl": 15250.75,
  "roi": 0.4875,
  "sharpe_ratio": 1.85,
  "max_drawdown": -2500.00,
  "monthly_pl": [
    {"month": "Dec 2025", "pl": 15250.75}
  ]
}
```

---

## TRADING LOGIC

### Decision-Making Flow

```
┌─────────────────────────────────────┐
│  Every 60 Seconds                   │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  Fetch Market Data                  │
│  - Price, RSI, EMA, ATR, Volume    │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  Send to Gemini AI                  │
│  "What should we do?"               │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  AI Returns Decision                │
│  {action, confidence, entry, SL, TP}│
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  Validation Checks                  │
│ ✓ Confidence > 70%?                 │
│ ✓ Position not open?                │
│ ✓ Under max 3 positions?            │
│ ✓ Stop loss ≠ entry?                │
└────────────┬────────────────────────┘
             │
        ┌────┴───────┐
        │             │
   All ✓ │         Not ✓ │
        │             │
        ▼             ▼
    ┌──────┐    ┌────────┐
    │ BUY  │    │  SKIP  │
    │/SELL │    │  HOLD  │
    └──────┘    └────────┘
        │
        ▼
┌─────────────────────────────────────┐
│  Execute Order on Binance           │
│  Market order for quantity          │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  Store Position                     │
│  - Track in active_positions        │
│  - Log to database                  │
│  - Monitor for SL/TP hits           │
└─────────────────────────────────────┘
```

### Technical Indicator Formulas

**RSI (Relative Strength Index)**
```
RSI = 100 - (100 / (1 + RS))
RS = Average Gain / Average Loss

Interpretation:
- RSI > 70 = Overbought (may reverse down)
- RSI < 30 = Oversold (may reverse up)
- 30-70 = Neutral
```

**EMA (Exponential Moving Average)**
```
EMA = Price × k + EMA(previous) × (1 - k)
k = 2 / (Period + 1)

Fast EMA (9) > Slow EMA (21) = BULLISH
Fast EMA (9) < Slow EMA (21) = BEARISH
```

**ATR (Average True Range)**
```
TR = max(High - Low, |High - Close|, |Low - Close|)
ATR = SMA of TR over 14 periods

Stop Loss = Entry - (ATR × 1.5)
Take Profit = Entry + (ATR × 1.5)
```

**Volume Ratio**
```
Current Volume / 20-candle Average
Need > 1.2x average = Volume confirmation
```

---

## AI INTEGRATION

### Gemini AI Setup

**API Reference:**
- Provider: Google AI (Free tier available)
- Model: `gemini-2.0-flash-exp` (fast, cheap)
- Rate Limit: 60 requests per minute (free)
- Cost: FREE with daily limits

**Prompt Engineering:**

The AI receives a carefully crafted prompt:

```
You are an expert cryptocurrency scalping trader analyzing BTCUSDT.

CURRENT MARKET STATE:
- Price: $42,500.00
- RSI(14): 65.25 (approaching overbought at 70)
- EMA(9): $42,400 > EMA(21): $42,200 (bullish)
- ATR(14): $150 (volatility measure)
- Volume: 125.5 vs Avg 100.2 = 1.25x (above average)
- Trend: BULLISH (9EMA > 21EMA)

DECISION RULES:
1. BUY when:
   - Fast EMA > Slow EMA (confirmed uptrend)
   - RSI < 70 (room to go higher)
   - Volume > 1.2x average (confirmation)
   - Price above both EMAs

2. SELL when:
   - Fast EMA < Slow EMA (confirmed downtrend)
   - RSI > 30 (room to go lower)
   - Volume > 1.2x average (confirmation)
   - Price below both EMAs

3. HOLD:
   - Mixed signals
   - Low volume
   - No clear trend

RISK MANAGEMENT:
- Entry: Current price
- Stop Loss: Entry - (ATR × 1.5)
- Take Profit: Entry + (ATR × 1.5)
- Risk/Reward minimum: 1:2

RESPOND IN EXACT JSON (no markdown, no explanations):
{
  "action": "BUY|SELL|HOLD",
  "confidence": 0.0-1.0,
  "entry_price": <number>,
  "stop_loss": <number>,
  "take_profit": <number>,
  "reasoning": "<brief explanation>"
}
```

### Response Parsing

```python
def _parse_response(self, response_text: str) -> Dict:
    """Extract JSON from AI response"""
    # AI might return markdown code blocks
    if '```' in response_text:
        response_text = response_text.split('```')[1]
        if response_text.startswith('json'):
            response_text = response_text[4:]
    
    # Parse JSON
    decision = json.loads(response_text)
    
    # Validate fields
    assert decision['action'] in ['BUY', 'SELL', 'HOLD']
    assert 0 <= decision['confidence'] <= 1
    
    return decision
```

### Backup AI Services

If Gemini fails:

**OpenAI (GPT-4)**
- Same prompt format
- Same JSON response expected
- More expensive but very reliable

**Anthropic (Claude)**
- Expert reasoning
- Reliable API
- Good fallback option

**Config:**
```python
ENABLE_BACKUP_APIS = True

# In .env:
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Automatic retry sequence:
1. Try Gemini AI
2. If fails → Try OpenAI
3. If fails → Try Anthropic
4. If all fail → Return HOLD
```

---

## RISK MANAGEMENT

### Position Sizing Formula

```
Risk Amount = Account Balance × Risk Per Trade %
Risk Per Trade = 2% (configurable)

Position Size = Risk Amount / (Entry Price - Stop Loss)

Example:
- Account: $10,000
- Risk: 2% = $200
- Entry: $42,500
- Stop Loss: $42,100
- Distance: $400

Quantity = $200 / $400 = 0.5 BTC (if minimum is 0.001)
```

### Stop Loss & Take Profit

**ATR-Based (Adaptive to Volatility)**

```
ATR = Average True Range over 14 periods
     (measures volatility)

Stop Loss = Entry - (ATR × 1.5)
Take Profit = Entry + (ATR × 1.5)

High Volatility:
- ATR = $500 → SL/TP distance = $750
- Wider stops, but higher potential reward

Low Volatility:
- ATR = $50 → SL/TP distance = $75
- Tighter stops, faster execution
```

### Daily Risk Limits

```
Max Simultaneous Positions: 3
Max Risk Per Trade: 2%
Max Daily Loss: 5% (stop trading if hit)

Example with $10,000 account:
- Trade 1: Risk $200 (2%)
- Trade 2: Risk $200 (2%)
- Trade 3: Risk $200 (2%)

Total daily risk = $600 (6% max, but we stop at 5%)
```

### Confidence Filtering

```
Only execute if:
AI Confidence ≥ 70%

Why 70%?
- Not too strict (miss good trades)
- Not too loose (take bad trades)
- Balances win rate and frequency

Example:
- AI says: action=BUY, confidence=0.65
- Status: SKIPPED (below 70% threshold)
```

---

## DATABASE STRUCTURE

### SQLite Database Location

```
data/trading_bot.db
```

### Tables

#### 1. trades
```sql
CREATE TABLE trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,           -- 'BTCUSDT'
    action TEXT NOT NULL,           -- 'BUY' or 'SELL'
    entry_price REAL NOT NULL,      -- 42500.00
    exit_price REAL,                -- 42650.50 (NULL if open)
    quantity REAL NOT NULL,         -- 0.001
    entry_time TEXT NOT NULL,       -- ISO format
    exit_time TEXT,                 -- NULL if open
    profit_loss REAL,               -- NULL if open
    profit_loss_percent REAL,       -- NULL if open
    confidence REAL,                -- 0.85
    reasoning TEXT,                 -- 'Bullish EMA...'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 2. positions
```sql
CREATE TABLE positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    action TEXT NOT NULL,           -- 'BUY' or 'SELL'
    entry_price REAL NOT NULL,
    current_price REAL NOT NULL,
    stop_loss REAL NOT NULL,
    take_profit REAL NOT NULL,
    quantity REAL NOT NULL,
    entry_time TEXT NOT NULL,
    unrealized_pl REAL,
    unrealized_pl_percent REAL,
    status TEXT DEFAULT 'OPEN',     -- 'OPEN', 'CLOSED', 'STOPPED'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 3. analytics
```sql
CREATE TABLE analytics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,             -- '2025-12-27'
    total_trades INTEGER,
    winning_trades INTEGER,
    losing_trades INTEGER,
    daily_pl REAL,
    win_rate REAL,
    average_win REAL,
    average_loss REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Example Data

**trades table:**
```
| id | symbol  | action | entry_price | exit_price | quantity | profit_loss | confidence |
|----|---------|--------|------------|-----------|----------|------------|-----------|
| 1  | BTCUSDT | BUY    | 42500.00   | 42650.50  | 0.001    | 150.50    | 0.85      |
| 2  | BTCUSDT | SELL   | 42600.00   | 42400.00  | 0.001    | 200.00    | 0.78      |
| 3  | BTCUSDT | BUY    | 42450.00   | NULL      | 0.001    | NULL      | 0.72      |
```

### Querying

**Get today's P&L:**
```sql
SELECT SUM(profit_loss) as daily_pl
FROM trades
WHERE date(entry_time) = date('now')
AND exit_price IS NOT NULL;
```

**Get win rate:**
```sql
SELECT 
    COUNT(*) as total,
    SUM(CASE WHEN profit_loss > 0 THEN 1 ELSE 0 END) as wins,
    ROUND(100.0 * SUM(CASE WHEN profit_loss > 0 THEN 1 ELSE 0 END) / COUNT(*), 2) as win_rate
FROM trades
WHERE exit_price IS NOT NULL;
```

**Get open positions:**
```sql
SELECT *
FROM positions
WHERE status = 'OPEN';
```

---

## TROUBLESHOOTING

### Issue: "API Key Invalid"

**Error Message:**
```
401 Unauthorized - Invalid API Key
```

**Solutions:**
1. Check `.env` file has correct key
2. Get new key from https://testnet.binance.vision/
3. Ensure you're using TESTNET key (not live)
4. Check key is enabled for spot trading

### Issue: Gemini API Rate Limit

**Error Message:**
```
429 Too Many Requests - Rate limit exceeded
```

**Why:** Free tier has 60 requests/minute limit

**Solutions:**
1. Increase check interval (60→120 seconds)
2. Use backup AI service (enable backup APIs)
3. Wait 1 minute, it resets

**In config/settings.py:**
```python
TRADING_CONFIG['check_interval'] = 120  # Check every 2 minutes instead
ENABLE_BACKUP_APIS = True               # Use backup if primary fails
```

### Issue: "No Open Positions" When Dashboard Shows Trades

**Cause:** Trades are closed. Only OPEN positions show on dashboard.

**Solution:**
Check "Journal" tab to see closed trades history.

### Issue: React Dashboard Shows Blank Page

**Error:** Dashboard won't load

**Solutions:**
1. Did you run `build.bat` or `build.sh`?
   ```powershell
   cd frontend
   npm run build
   cd ..
   ```

2. Is Flask running?
   ```powershell
   python main.py
   ```

3. Clear browser cache
   - Press `Ctrl+Shift+Delete`
   - Clear cache
   - Reload page

4. Check console for errors
   - Press `F12`
   - Check "Console" tab

### Issue: Bot Not Trading

**Check:**
1. Is bot running?
   - Overview tab should show green "Running"

2. Is there enough balance?
   - Check account balance in Binance testnet

3. Is AI making decisions?
   - Check logs in terminal
   - Should see "🤖 AI Decision:" lines

4. Is confidence too low?
   - Increase: `min_confidence: 0.6` (default 0.7)

5. Are we at max positions?
   - Check "Positions" in Journal tab
   - Reduce: `max_positions: 5` (default 3)

### Issue: Trades Closing Immediately

**Cause:** Stop loss or take profit hit too quickly

**Solution:** Adjust ATR multiplier
```python
'atr_multiplier': 2.0  # Increase from 1.5 to 2.0 (wider stops)
```

### Issue: High Loss Rate

**Optimization Tips:**
1. Increase minimum confidence
   ```python
   'min_confidence': 0.80  # Stricter filtering
   ```

2. Adjust RSI thresholds
   ```python
   'rsi_overbought': 75,   # Less aggressive
   'rsi_oversold': 25
   ```

3. Increase volume requirement
   ```python
   'volume_threshold': 1.5  # Require 1.5x volume
   ```

4. Use wider stops
   ```python
   'atr_multiplier': 2.5
   ```

### Common Log Messages Explained

| Message | Meaning | Action |
|---------|---------|--------|
| `🤖 AI Decision: BUY` | AI says buy | May execute if conditions met |
| `Low confidence: 0.45` | AI not confident | Trade skipped |
| `Position already open` | Can't open another | Wait for close |
| `Max positions reached` | Already 3 open | Close one to trade more |
| `Order placed: 0.001 BTC` | Trade executed | Tracking in database |
| `Gemini AI error` | Primary AI failed | Trying backup AI |

---

## PERFORMANCE OPTIMIZATION

### Speed Up Checking

**Faster Decisions (every 30 seconds):**
```python
'check_interval': 30  # Instead of 60
```

**Pros:** More trading opportunities  
**Cons:** More API calls, more database writes

### Reduce API Calls

**Every 2 minutes:**
```python
'check_interval': 120
```

**Pros:** Lower API usage, fewer Gemini charges  
**Cons:** Miss some quick moves

### Monitor Performance

**Check logs:**
```powershell
# Windows
Get-Content logs/app.log -Tail 50

# Linux/Mac
tail -50 logs/app.log
```

**Key Metrics to Watch:**
- Win rate (target: >50%)
- Profit factor (target: >1.5)
- Average win vs average loss (target: win ≥ loss)
- Drawdown (how low can it go)

---

## SECURITY BEST PRACTICES

### Protect Your Keys

**DO:**
- ✅ Store keys in `.env` file
- ✅ Add `.env` to `.gitignore`
- ✅ Use testnet (not real money)
- ✅ Limit API key permissions (spot trading only)
- ✅ Whitelist your IP on Binance

**DON'T:**
- ❌ Commit `.env` to Git
- ❌ Share API keys
- ❌ Post keys in Discord/Slack
- ❌ Use in public GitHub repo
- ❌ Enable withdrawal permissions

### `.gitignore` File

Create `.gitignore` in root:
```
.env
__pycache__/
*.pyc
.DS_Store
logs/
data/
node_modules/
venv/
.vscode/
.idea/
```

### Run in Testnet Only

**Current config uses testnet:**
```python
BINANCE_USE_TESTNET = True  # ALWAYS true for learning!
```

**To go live (DANGEROUS):**
- Set `BINANCE_USE_TESTNET = False`
- Use real API keys
- Risk real money
- **NOT RECOMMENDED** without extensive testing

---

## NEXT STEPS & IMPROVEMENTS

### Possible Enhancements

1. **Multiple Symbols**
   - Trade ETHUSDT, XRPUSDT, etc
   - Diversify risk across pairs

2. **Advanced Indicators**
   - Bollinger Bands
   - MACD histogram
   - Stochastic RSI

3. **Machine Learning**
   - Train neural network on historical data
   - Predict next 5-minute move
   - Beat simple rules-based approach

4. **Slack/Email Alerts**
   - Notify trades via Slack
   - Daily summary email
   - Alert on big moves

5. **Web Push Notifications**
   - Browser notifications
   - Real-time alerts
   - Mobile-friendly

6. **Advanced Risk**
   - Dynamic position sizing
   - Correlation analysis
   - Portfolio heat mapping

---

## SUPPORT & RESOURCES

### Documentation
- [Binance API Docs](https://binance-docs.github.io/apidocs/)
- [Gemini AI Docs](https://ai.google.dev/docs)
- [React Docs](https://react.dev)
- [Python Pandas](https://pandas.pydata.org/)

### Communities
- Binance Dev Community
- Crypto Trading Discord servers
- Reddit: r/algotrading

### Learning
- [Technical Analysis Course](https://www.investopedia.com/terms/t/technicalanalysis.asp)
- [Crypto Trading Basics](https://www.coinbase.com/learn)
- [Python for Finance](https://www.datacamp.com/)

---

## LICENSE & DISCLAIMER

**FREE & OPEN SOURCE**

Use at your own risk. This bot trades on Binance TESTNET (no real money). Even in testnet, trading logic may not be profitable. Always test thoroughly before considering live trading.

**⚠️ IMPORTANT:**
- This is educational software
- No guarantee of profitability
- Past performance ≠ future results
- Only trade what you can afford to lose
- Start small and scale gradually
- Use stop losses always

---

## CONTACT & CONTRIBUTIONS

Found a bug? Want to contribute?

1. Open issue on GitHub
2. Provide error logs
3. Describe steps to reproduce
4. Be specific and detailed

---

**Last Updated:** December 27, 2025  
**Version:** 1.0 Production Ready  
**Status:** Actively Maintained

---

### QUICK REFERENCE CHECKLIST

Before running the bot:

- [ ] Python 3.10+ installed
- [ ] Node.js 14+ installed
- [ ] `.env` file created with API keys
- [ ] `pip install -r requirements.txt` completed
- [ ] `cd frontend && npm install && cd ..` completed
- [ ] `frontend/build.bat` or `build.sh` executed
- [ ] Binance testnet account created
- [ ] Gemini API key obtained
- [ ] No real money involved
- [ ] Logs folder exists
- [ ] Data folder exists

Ready to go!

```powershell
python main.py
```

Then open: http://localhost:5000

🚀 Happy trading! (on testnet)
