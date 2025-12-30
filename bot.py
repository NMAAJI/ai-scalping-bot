"""
AI-Powered Binance Testnet Trading Bot
100% FREE - No Subscriptions Required
Uses Gemini AI for trade decisions
"""

from flask import Flask, render_template_string, jsonify
from binance.client import Client
from binance.enums import *
from google import genai
import pandas as pd
import time
import json
import logging
from datetime import datetime
from threading import Thread

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# ============ CONFIGURATION ============
# Binance Testnet API Keys (Get from: https://testnet.binance.vision/)
BINANCE_API_KEY = 'YOUR_BINANCE_TESTNET_API_KEY'
BINANCE_API_SECRET = 'YOUR_BINANCE_TESTNET_SECRET_KEY'

# Binance Testnet URLs
BINANCE_TESTNET_URL = 'https://testnet.binance.vision'

# Gemini AI
GEMINI_API_KEY = 'AIzaSyA1W-qzVyR_hC_Nj-RkvTsVzfh0hDRZyVA'

# Trading Configuration
TRADING_CONFIG = {
    'symbol': 'BTCUSDT',
    'timeframe': '1m',  # 1 minute candles
    'risk_per_trade': 0.02,  # 2%
    'max_positions': 3,
    'min_confidence': 0.7,
    'check_interval': 60,  # Check every 60 seconds
    
    # Indicator Settings
    'rsi_period': 14,
    'rsi_overbought': 70,
    'rsi_oversold': 30,
    'ema_fast': 9,
    'ema_slow': 21,
    'atr_period': 14,
    'atr_multiplier': 1.5,
    'volume_threshold': 1.2
}

# Initialize Binance Client (Testnet)
client = Client(BINANCE_API_KEY, BINANCE_API_SECRET, testnet=True)
client.API_URL = BINANCE_TESTNET_URL

# Initialize Gemini AI
genai_client = genai.Client(api_key=GEMINI_API_KEY)

# Store positions and trades
active_positions = {}
trade_history = []
bot_running = False

# ============ TECHNICAL INDICATORS ============

def calculate_rsi(prices, period=14):
    """Calculate RSI indicator"""
    deltas = pd.Series(prices).diff()
    gain = (deltas.where(deltas > 0, 0)).rolling(window=period).mean()
    loss = (-deltas.where(deltas < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1]

def calculate_ema(prices, period):
    """Calculate EMA indicator"""
    return pd.Series(prices).ewm(span=period, adjust=False).mean().iloc[-1]

def calculate_atr(high, low, close, period=14):
    """Calculate ATR indicator"""
    df = pd.DataFrame({'high': high, 'low': low, 'close': close})
    df['tr'] = pd.concat([
        df['high'] - df['low'],
        abs(df['high'] - df['close'].shift()),
        abs(df['low'] - df['close'].shift())
    ], axis=1).max(axis=1)
    atr = df['tr'].rolling(window=period).mean().iloc[-1]
    return atr

def get_market_data():
    """Fetch real-time market data from Binance"""
    try:
        # Get klines (candlestick data)
        klines = client.get_klines(
            symbol=TRADING_CONFIG['symbol'],
            interval=TRADING_CONFIG['timeframe'],
            limit=100
        )
        
        # Extract data
        closes = [float(k[4]) for k in klines]
        highs = [float(k[2]) for k in klines]
        lows = [float(k[3]) for k in klines]
        volumes = [float(k[5]) for k in klines]
        
        current_price = closes[-1]
        
        # Calculate indicators
        rsi = calculate_rsi(closes, TRADING_CONFIG['rsi_period'])
        ema_fast = calculate_ema(closes, TRADING_CONFIG['ema_fast'])
        ema_slow = calculate_ema(closes, TRADING_CONFIG['ema_slow'])
        atr = calculate_atr(highs, lows, closes, TRADING_CONFIG['atr_period'])
        
        avg_volume = sum(volumes[-20:]) / 20
        current_volume = volumes[-1]
        
        # Determine trend
        trend = "bullish" if ema_fast > ema_slow else "bearish" if ema_fast < ema_slow else "neutral"
        
        market_data = {
            'price': current_price,
            'rsi': rsi,
            'ema_fast': ema_fast,
            'ema_slow': ema_slow,
            'atr': atr,
            'volume': current_volume,
            'avg_volume': avg_volume,
            'trend': trend,
            'timestamp': datetime.now().isoformat()
        }
        
        return market_data
        
    except Exception as e:
        logger.error(f"Error fetching market data: {e}")
        return None

# ============ AI ANALYSIS ============

def analyze_with_gemini(market_data):
    """Use Gemini AI to analyze market and make trading decision"""
    try:
        prompt = f"""
You are an expert cryptocurrency scalping trader. Analyze this market data and make a trading decision.

MARKET DATA:
- Symbol: {TRADING_CONFIG['symbol']}
- Current Price: ${market_data['price']:.2f}
- RSI: {market_data['rsi']:.2f}
- Fast EMA (9): ${market_data['ema_fast']:.2f}
- Slow EMA (21): ${market_data['ema_slow']:.2f}
- ATR: ${market_data['atr']:.2f}
- Current Volume: {market_data['volume']:.0f}
- Average Volume: {market_data['avg_volume']:.0f}
- Trend: {market_data['trend']}

TRADING RULES:
1. BUY when: Fast EMA crosses above Slow EMA, RSI < {TRADING_CONFIG['rsi_overbought']}, volume > average, bullish trend
2. SELL when: Fast EMA crosses below Slow EMA, RSI > {TRADING_CONFIG['rsi_oversold']}, volume > average, bearish trend
3. HOLD when: No clear signal or mixed indicators
4. Risk-reward ratio minimum 1:2
5. Use ATR for stop loss and take profit calculation

Respond in EXACT JSON format (no markdown):
{{
    "action": "BUY" or "SELL" or "HOLD",
    "confidence": 0.0 to 1.0,
    "entry_price": {market_data['price']},
    "stop_loss": price level,
    "take_profit": price level,
    "reasoning": "brief explanation"
}}
"""
        
        response = genai_client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=prompt
        )
        
        response_text = response.text.strip()
        
        # Clean response
        if '```json' in response_text:
            response_text = response_text.split('```json')[1].split('```')[0].strip()
        elif '```' in response_text:
            response_text = response_text.split('```')[1].split('```')[0].strip()
        
        ai_decision = json.loads(response_text)
        logger.info(f"🤖 AI Decision: {ai_decision['action']} (Confidence: {ai_decision['confidence']:.2%})")
        
        return ai_decision
        
    except Exception as e:
        logger.error(f"Gemini AI error: {e}")
        return {
            'action': 'HOLD',
            'confidence': 0,
            'reasoning': f'Error: {str(e)}'
        }

# ============ TRADING EXECUTION ============

def execute_trade(ai_decision, market_data):
    """Execute trade on Binance Testnet"""
    try:
        symbol = TRADING_CONFIG['symbol']
        
        # Check if position already exists
        if symbol in active_positions:
            logger.info(f"Position already open for {symbol}")
            return {"status": "skipped", "reason": "Position exists"}
        
        # Check confidence
        if ai_decision['confidence'] < TRADING_CONFIG['min_confidence']:
            logger.info(f"Low confidence: {ai_decision['confidence']:.2%}")
            return {"status": "skipped", "reason": "Low confidence"}
        
        # Check max positions
        if len(active_positions) >= TRADING_CONFIG['max_positions']:
            logger.info("Max positions reached")
            return {"status": "skipped", "reason": "Max positions"}
        
        action = ai_decision['action']
        
        if action == 'HOLD':
            return {"status": "hold"}
        
        # Get account balance
        account = client.get_account()
        usdt_balance = float([b for b in account['balances'] if b['asset'] == 'USDT'][0]['free'])
        
        # Calculate position size (2% risk)
        risk_amount = usdt_balance * TRADING_CONFIG['risk_per_trade']
        price_risk = abs(ai_decision['entry_price'] - ai_decision['stop_loss'])
        
        if price_risk == 0:
            return {"status": "error", "reason": "Invalid stop loss"}
        
        quantity = risk_amount / price_risk
        
        # Place order (market order for simplicity)
        order_side = SIDE_BUY if action == 'BUY' else SIDE_SELL
        
        # NOTE: This is testnet - safe to test!
        order = client.create_order(
            symbol=symbol,
            side=order_side,
            type=ORDER_TYPE_MARKET,
            quantity=round(quantity, 6)
        )
        
        # Store position
        position = {
            'symbol': symbol,
            'action': action,
            'entry_price': ai_decision['entry_price'],
            'stop_loss': ai_decision['stop_loss'],
            'take_profit': ai_decision['take_profit'],
            'quantity': quantity,
            'entry_time': datetime.now().isoformat(),
            'confidence': ai_decision['confidence'],
            'reasoning': ai_decision['reasoning'],
            'order_id': order['orderId']
        }
        
        active_positions[symbol] = position
        
        logger.info(f"✅ Trade Executed: {action} {quantity:.6f} {symbol} @ ${ai_decision['entry_price']:.2f}")
        logger.info(f"   SL: ${ai_decision['stop_loss']:.2f} | TP: ${ai_decision['take_profit']:.2f}")
        
        return {"status": "executed", "position": position}
        
    except Exception as e:
        logger.error(f"Trade execution error: {e}")
        return {"status": "error", "reason": str(e)}

def check_exit_conditions():
    """Check if any positions should be closed"""
    try:
        for symbol, position in list(active_positions.items()):
            # Get current price
            ticker = client.get_symbol_ticker(symbol=symbol)
            current_price = float(ticker['price'])
            
            should_close = False
            exit_reason = None
            
            # Check stop loss
            if position['action'] == 'BUY' and current_price <= position['stop_loss']:
                should_close = True
                exit_reason = 'stop_loss'
            elif position['action'] == 'SELL' and current_price >= position['stop_loss']:
                should_close = True
                exit_reason = 'stop_loss'
            
            # Check take profit
            if position['action'] == 'BUY' and current_price >= position['take_profit']:
                should_close = True
                exit_reason = 'take_profit'
            elif position['action'] == 'SELL' and current_price <= position['take_profit']:
                should_close = True
                exit_reason = 'take_profit'
            
            if should_close:
                close_position(symbol, current_price, exit_reason)
                
    except Exception as e:
        logger.error(f"Error checking exit conditions: {e}")

def close_position(symbol, current_price, reason):
    """Close position and record trade"""
    try:
        if symbol not in active_positions:
            return
        
        position = active_positions[symbol]
        
        # Calculate P&L
        if position['action'] == 'BUY':
            pnl = (current_price - position['entry_price']) * position['quantity']
        else:
            pnl = (position['entry_price'] - current_price) * position['quantity']
        
        pnl_percentage = (pnl / (position['entry_price'] * position['quantity'])) * 100
        
        # Close position on exchange
        close_side = SIDE_SELL if position['action'] == 'BUY' else SIDE_BUY
        client.create_order(
            symbol=symbol,
            side=close_side,
            type=ORDER_TYPE_MARKET,
            quantity=position['quantity']
        )
        
        # Record trade
        trade = {
            **position,
            'exit_price': current_price,
            'exit_time': datetime.now().isoformat(),
            'exit_reason': reason,
            'pnl': pnl,
            'pnl_percentage': pnl_percentage
        }
        
        trade_history.append(trade)
        del active_positions[symbol]
        
        logger.info(f"🔴 Position Closed: {symbol} | {reason}")
        logger.info(f"   P&L: ${pnl:.2f} ({pnl_percentage:.2f}%)")
        
    except Exception as e:
        logger.error(f"Error closing position: {e}")

# ============ BOT MAIN LOOP ============

def trading_bot_loop():
    """Main bot loop - runs continuously"""
    global bot_running
    
    logger.info("🚀 AI Trading Bot Started!")
    logger.info(f"📊 Trading: {TRADING_CONFIG['symbol']}")
    logger.info(f"⏱️  Timeframe: {TRADING_CONFIG['timeframe']}")
    logger.info(f"💰 Risk Per Trade: {TRADING_CONFIG['risk_per_trade']*100}%")
    
    while bot_running:
        try:
            # Get market data
            market_data = get_market_data()
            
            if market_data:
                logger.info(f"📊 Price: ${market_data['price']:.2f} | RSI: {market_data['rsi']:.1f} | Trend: {market_data['trend']}")
                
                # Check exit conditions first
                check_exit_conditions()
                
                # Get AI analysis
                ai_decision = analyze_with_gemini(market_data)
                
                # Execute trade if conditions met
                if ai_decision['action'] != 'HOLD':
                    execute_trade(ai_decision, market_data)
            
            # Wait before next check
            time.sleep(TRADING_CONFIG['check_interval'])
            
        except Exception as e:
            logger.error(f"Error in bot loop: {e}")
            time.sleep(60)

# ============ WEB DASHBOARD ============

DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Trading Bot Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0a0e27; color: #fff; padding: 20px; }
        .container { max-width: 1400px; margin: 0 auto; }
        h1 { text-align: center; margin-bottom: 30px; color: #00d4ff; }
        .status { background: #1a1f3a; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 30px; }
        .stat-card { background: #1a1f3a; padding: 20px; border-radius: 10px; text-align: center; }
        .stat-value { font-size: 32px; font-weight: bold; color: #00d4ff; }
        .stat-label { color: #8b92b0; margin-top: 5px; }
        .positions { background: #1a1f3a; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
        .position { background: #252b4a; padding: 15px; border-radius: 8px; margin-bottom: 10px; }
        .buy { border-left: 4px solid #00ff88; }
        .sell { border-left: 4px solid #ff4466; }
        .trades { background: #1a1f3a; padding: 20px; border-radius: 10px; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #2a3155; }
        th { color: #00d4ff; }
        .profit { color: #00ff88; }
        .loss { color: #ff4466; }
        .btn { background: #00d4ff; color: #0a0e27; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; }
        .btn:hover { background: #00b8e6; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 AI Trading Bot Dashboard</h1>
        
        <div class="status">
            <h2>Bot Status: <span id="bot-status">Loading...</span></h2>
            <button class="btn" onclick="toggleBot()">Start/Stop Bot</button>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value" id="current-price">-</div>
                <div class="stat-label">Current Price</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="active-positions">0</div>
                <div class="stat-label">Active Positions</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="total-trades">0</div>
                <div class="stat-label">Total Trades</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="win-rate">0%</div>
                <div class="stat-label">Win Rate</div>
            </div>
        </div>
        
        <div class="positions">
            <h2>Active Positions</h2>
            <div id="positions-list">No active positions</div>
        </div>
        
        <div class="trades">
            <h2>Recent Trades</h2>
            <table>
                <thead>
                    <tr>
                        <th>Time</th>
                        <th>Action</th>
                        <th>Entry</th>
                        <th>Exit</th>
                        <th>P&L</th>
                        <th>%</th>
                    </tr>
                </thead>
                <tbody id="trades-list">
                    <tr><td colspan="6">No trades yet</td></tr>
                </tbody>
            </table>
        </div>
    </div>
    
    <script>
        function updateDashboard() {
            fetch('/api/status')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('bot-status').textContent = data.bot_running ? 'RUNNING' : 'STOPPED';
                    document.getElementById('active-positions').textContent = data.active_positions;
                    document.getElementById('total-trades').textContent = data.total_trades;
                    document.getElementById('win-rate').textContent = data.win_rate + '%';
                    
                    // Update positions
                    const posDiv = document.getElementById('positions-list');
                    if (data.positions.length === 0) {
                        posDiv.innerHTML = 'No active positions';
                    } else {
                        posDiv.innerHTML = data.positions.map(p => 
                            `<div class="position ${p.action.toLowerCase()}">
                                <strong>${p.action} ${p.symbol}</strong> @ $${p.entry_price.toFixed(2)}<br>
                                SL: $${p.stop_loss.toFixed(2)} | TP: $${p.take_profit.toFixed(2)}<br>
                                Confidence: ${(p.confidence*100).toFixed(0)}%
                            </div>`
                        ).join('');
                    }
                    
                    // Update trades
                    const tbody = document.getElementById('trades-list');
                    if (data.recent_trades.length === 0) {
                        tbody.innerHTML = '<tr><td colspan="6">No trades yet</td></tr>';
                    } else {
                        tbody.innerHTML = data.recent_trades.map(t => 
                            `<tr>
                                <td>${new Date(t.exit_time).toLocaleString()}</td>
                                <td>${t.action}</td>
                                <td>$${t.entry_price.toFixed(2)}</td>
                                <td>$${t.exit_price.toFixed(2)}</td>
                                <td class="${t.pnl >= 0 ? 'profit' : 'loss'}">$${t.pnl.toFixed(2)}</td>
                                <td class="${t.pnl_percentage >= 0 ? 'profit' : 'loss'}">${t.pnl_percentage.toFixed(2)}%</td>
                            </tr>`
                        ).join('');
                    }
                });
        }
        
        function toggleBot() {
            fetch('/api/toggle', {method: 'POST'})
                .then(r => r.json())
                .then(data => {
                    alert('Bot ' + (data.running ? 'started' : 'stopped'));
                    updateDashboard();
                });
        }
        
        setInterval(updateDashboard, 3000);
        updateDashboard();
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    return render_template_string(DASHBOARD_HTML)

@app.route('/api/status')
def api_status():
    winning_trades = sum(1 for t in trade_history if t.get('pnl', 0) > 0)
    total = len(trade_history)
    win_rate = (winning_trades / total * 100) if total > 0 else 0
    
    return jsonify({
        'bot_running': bot_running,
        'active_positions': len(active_positions),
        'total_trades': len(trade_history),
        'win_rate': round(win_rate, 1),
        'positions': list(active_positions.values()),
        'recent_trades': trade_history[-10:]
    })

@app.route('/api/toggle', methods=['POST'])
def toggle_bot():
    global bot_running
    bot_running = not bot_running
    
    if bot_running:
        Thread(target=trading_bot_loop, daemon=True).start()
    
    return jsonify({'running': bot_running})

if __name__ == '__main__':
    logger.info("Starting AI Trading Bot Server...")
    logger.info("Dashboard will be available at: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)