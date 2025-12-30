"""
AI-Powered Binance Testnet Trading Bot
Main Entry Point

100% FREE - No Subscriptions Required
Uses Gemini AI for trade decisions
"""

import logging
import time
import os
from threading import Thread
from flask import Flask, render_template, send_from_directory, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from config.settings import (
    BINANCE_API_KEY, BINANCE_API_SECRET, BINANCE_TESTNET_URL,
    GEMINI_API_KEY, TRADING_CONFIG, LOG_LEVEL, LOG_FORMAT,
    FLASK_HOST, FLASK_PORT, FLASK_DEBUG, validate_api_keys,
    AUTONOMOUS_MODE, ENABLE_BACKUP_APIS,
    OPENAI_API_KEY, ANTHROPIC_API_KEY, TOGETHER_API_KEY
)
from binance.client import Client
from market.data_fetcher import MarketDataFetcher
from ai.analyzer import GeminiAnalyzer
from ai.autonomous_engine import FullyAutonomousTrader
from trading.executor import TradeExecutor
from trading.auto_engine import AutoTradingEngine
from web.react_dashboard import REACT_DASHBOARD
from utils.helpers import setup_logging, ensure_directories_exist

# Configure logging
try:
    setup_logging(LOG_LEVEL, LOG_FORMAT)
except Exception as e:
    # Fallback for read-only filesystems (Vercel)
    logging.basicConfig(level=logging.INFO)
    logging.getLogger(__name__).warning(f"Could not setup file logging (likely read-only env): {e}")

logger = logging.getLogger(__name__)

# Initialize Flask app with static files configuration
app = Flask(
    __name__,
    static_folder=os.path.join(os.path.dirname(__file__), 'web', 'static'),
    static_url_path='/static',
    template_folder=os.path.join(os.path.dirname(__file__), 'web', 'templates')
)

# Enable CORS for API requests
CORS(app)

# Global state
bot_running = False
market_fetcher = None
ai_analyzer = None
trade_executor = None
auto_engine = None
autonomous_trader = None  # NEW: Fully autonomous AI trader
auto_thread = None

# Display startup mode
logger.info("=" * 70)
if AUTONOMOUS_MODE:
    logger.info("🤖 AUTONOMOUS MODE ENABLED - FULLY AUTOMATED AI TRADING")
    logger.info("⚠️ NO HUMAN INTERVENTION REQUIRED - DIRECT API DECISION EXECUTION")
else:
    logger.info("🎮 MANUAL MODE - HUMAN SUPERVISION REQUIRED")
logger.info("=" * 70)


def initialize_services() -> bool:
    """
    Initialize all bot services (Binance client, AI, etc.)
    
    Returns:
        True if initialization successful, False otherwise
    """
    global market_fetcher, ai_analyzer, trade_executor, auto_engine, autonomous_trader
    
    try:
        # Validate API keys
        if not validate_api_keys():
            logger.error("❌ API keys not configured properly!")
            logger.error("Please set environment variables:")
            logger.error("  - BINANCE_API_KEY")
            logger.error("  - BINANCE_API_SECRET")
            logger.error("  - GEMINI_API_KEY")
            return False
        
        # Initialize Binance client (Testnet)
        logger.info("Initializing Binance Testnet client...")
        binance_client = Client(BINANCE_API_KEY, BINANCE_API_SECRET, testnet=True)
        binance_client.API_URL = BINANCE_TESTNET_URL
        
        # Test connection
        account = binance_client.get_account()
        logger.info(f"✅ Connected to Binance Testnet")
        
        # Initialize market data fetcher
        market_fetcher = MarketDataFetcher(binance_client)
        logger.info("✅ Market data fetcher initialized")
        
        # Initialize AI analyzer
        ai_analyzer = GeminiAnalyzer(GEMINI_API_KEY)
        logger.info("✅ Gemini AI analyzer initialized")
        
        # Initialize trade executor
        trade_executor = TradeExecutor(binance_client)
        logger.info("✅ Trade executor initialized")
        
        # Initialize auto-trading engine
        auto_engine = AutoTradingEngine(market_fetcher, ai_analyzer, trade_executor)
        trade_executor.auto_engine = auto_engine
        trade_executor.bot_running = False
        logger.info("✅ Auto-trading engine initialized")
        
        # Initialize autonomous AI trader (if enabled)
        if AUTONOMOUS_MODE:
            logger.info("🤖 Initializing Autonomous AI Trader with backup services...")
            autonomous_trader = FullyAutonomousTrader(market_fetcher, trade_executor)
            
            # Configure backup AI services if enabled
            if ENABLE_BACKUP_APIS:
                logger.info("⚙️ Configuring backup AI services...")
                
                if OPENAI_API_KEY:
                    autonomous_trader.backup_service.add_service(
                        'openai', OPENAI_API_KEY, 'openai', priority=1
                    )
                    logger.info("✅ OpenAI backup service configured")
                
                if ANTHROPIC_API_KEY:
                    autonomous_trader.backup_service.add_service(
                        'anthropic', ANTHROPIC_API_KEY, 'anthropic', priority=2
                    )
                    logger.info("✅ Anthropic backup service configured")
                
                if TOGETHER_API_KEY:
                    autonomous_trader.backup_service.add_service(
                        'together', TOGETHER_API_KEY, 'together', priority=3
                    )
                    logger.info("✅ Together AI backup service configured")
                
                status = autonomous_trader.backup_service.get_status()
                logger.info(f"🔄 Backup services status: {status}")
            
            logger.info("✅ Autonomous AI Trader initialized with full decision autonomy")
        
        # Create directories
        try:
            ensure_directories_exist(['logs', 'data'])
        except Exception as e:
            logger.warning(f"Skipping directory creation (read-only env): {e}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Initialization failed: {e}")
        return False


def trading_bot_loop() -> None:
    """Main bot trading loop - runs continuously"""
    global bot_running, autonomous_trader
    
    logger.info("🚀 AI Trading Bot Started!")
    logger.info(f"📊 Trading: {TRADING_CONFIG['symbol']}")
    logger.info(f"⏱️  Timeframe: {TRADING_CONFIG['timeframe']}")
    logger.info(f"💰 Risk Per Trade: {TRADING_CONFIG['risk_per_trade']*100}%")
    logger.info(f"🎯 Min Confidence: {TRADING_CONFIG['min_confidence']*100}%")
    
    # If autonomous mode is enabled, start the autonomous trader
    if AUTONOMOUS_MODE and autonomous_trader:
        logger.info("🤖 Starting Autonomous AI Trader...")
        autonomous_trader.start()
        
        # Monitor autonomous trader
        while bot_running:
            try:
                # Get autonomous trader status
                status = autonomous_trader.get_status()
                
                # Log periodic status updates
                if status['trades_executed'] > 0:
                    logger.info(
                        f"🤖 Autonomous Status | "
                        f"Trades Executed: {status['trades_executed']} | "
                        f"Last Decision: {status['last_decision_time']} | "
                        f"Status: {'ACTIVE' if status['is_running'] else 'STOPPED'}"
                    )
                
                time.sleep(TRADING_CONFIG['check_interval'])
                
            except Exception as e:
                logger.error(f"Error monitoring autonomous trader: {e}")
                time.sleep(60)
        
        # Stop autonomous trader on exit
        if autonomous_trader:
            autonomous_trader.stop()
    else:
        # Manual trading mode
        logger.info("🎮 Starting Manual Trading Mode...")
        while bot_running:
            try:
                # Get market data
                market_data = market_fetcher.get_market_data()
                
                if market_data:
                    logger.info(
                        f"📊 Price: ${market_data['price']:.2f} | "
                        f"RSI: {market_data['rsi']:.1f} | "
                        f"Trend: {market_data['trend']}"
                    )
                    
                    # Check exit conditions first
                    trade_executor.check_exit_conditions()
                    
                    # Get AI analysis
                    ai_decision = ai_analyzer.analyze_market(market_data)
                    
                    # Execute trade if conditions met
                    if ai_decision['action'] != 'HOLD':
                        result = trade_executor.execute_trade(ai_decision, market_data)
                        logger.info(f"Trade execution result: {result['status']}")
                
                # Wait before next check
                time.sleep(TRADING_CONFIG['check_interval'])
                
            except Exception as e:
                logger.error(f"Error in bot loop: {e}")
                time.sleep(60)
    
    logger.info("🛑 AI Trading Bot Stopped!")


def start_bot() -> None:
    """Start the trading bot"""
    global bot_running
    
    if bot_running:
        logger.warning("Bot is already running!")
        return
    
    bot_running = True
    trade_executor.bot_running = True
    
    # Start bot in background thread
    bot_thread = Thread(target=trading_bot_loop, daemon=True)
    bot_thread.start()
    logger.info("Bot thread started")


def stop_bot() -> None:
    """Stop the trading bot"""
    global bot_running
    bot_running = False
    if trade_executor:
        trade_executor.bot_running = False
    logger.info("Bot stopping...")


def main() -> None:
    """Main entry point"""
    global auto_thread
    
    logger.info("=" * 60)
    logger.info("🤖 AI-Powered Binance Trading Bot")
    logger.info("=" * 60)
    
    # Initialize services
    if not initialize_services():
        logger.error("Failed to initialize services. Exiting.")
        return
    
    # Start auto-trading background thread (but don't start auto-trading yet)
    auto_thread = Thread(target=auto_engine.monitor_market, daemon=True)
    auto_thread.start()
    logger.info("✅ Auto-trading monitor thread started (monitoring, not trading yet)")

    # =====================================================
    # React Frontend Routes
    # =====================================================
    
    @app.route('/')
    def serve_dashboard():
        """Serve React dashboard (check for built app, fallback to embedded React)"""
        # Try to serve from built React app if it exists
        if os.path.exists(os.path.join(app.template_folder, 'index.html')):
            return render_template('index.html')
        # Fallback to embedded React dashboard
        return REACT_DASHBOARD
    
    @app.route('/static/<path:path>')
    def serve_static(path):
        """Serve static files (JS, CSS, images)"""
        return send_from_directory(app.static_folder, path)
    
    # =====================================================
    # API Endpoints for React Dashboard
    # =====================================================
    
    from flask import render_template_string, jsonify
    
    # API endpoints for React dashboard
    @app.route('/api/status')
    def api_status():
        """Get bot status and statistics"""
        stats = trade_executor.get_statistics()
        
        # Get auto-engine running status
        auto_running = False
        if hasattr(auto_engine, 'is_running'):
            auto_running = auto_engine.is_running
        
        return jsonify({
            'bot_running': auto_running,
            'price': getattr(trade_executor, 'current_price', 0),
            'active_positions': stats['active_positions'],
            'total_trades': stats['total_trades'],
            'winning_trades': stats['winning_trades'],
            'win_rate': stats['win_rate'],
            'total_pnl': stats['total_pnl'],
            'today_pnl': stats.get('today_pnl', 0),
            'avg_profit': stats.get('avg_profit', 0),
            'avg_loss': stats.get('avg_loss', 0),
            'positions': list(trade_executor.active_positions.values()),
            'recent_trades': trade_executor.trade_history[-10:]
        })
    
    @app.route('/api/trade-history')
    def get_trade_history():
        """Get trade history for chart markers"""
        trades = []
        
        if hasattr(trade_executor, 'trade_history') and trade_executor.trade_history:
            trades = [
                {
                    'entry_price': t.get('entry_price', 0),
                    'exit_price': t.get('exit_price', None),
                    'quantity': t.get('quantity', 0),
                    'entry_time': t.get('entry_time', ''),
                    'exit_time': t.get('exit_time', ''),
                    'pnl': t.get('pnl', 0),
                    'action': t.get('action', 'BUY')
                }
                for t in trade_executor.trade_history[-20:]
            ]
        
        if hasattr(trade_executor, 'active_positions'):
            for pos_id, pos in trade_executor.active_positions.items():
                trades.append({
                    'entry_price': pos.get('entry_price', 0),
                    'exit_price': None,
                    'quantity': pos.get('quantity', 0),
                    'entry_time': pos.get('entry_time', ''),
                    'exit_time': '',
                    'pnl': 0,
                    'action': pos.get('action', 'BUY')
                })
        
        return jsonify({'trades': trades})
    
    @app.route('/api/analytics')
    def get_analytics():
        """Get analytics data for charts"""
        try:
            from utils.database import TradingDatabase
            db = TradingDatabase()
            
            analytics = db.get_analytics_data()
            win_loss = db.get_win_loss_breakdown()
            top_symbols = db.get_top_performing_symbols(5)
            pnl_by_date = db.get_pnl_by_date(30)
            daily_stats = db.get_daily_stats(30)
            
            return jsonify({
                'total_trades': analytics.get('total_trades', 0),
                'winning_trades': analytics.get('winning_trades', 0),
                'win_rate': analytics.get('win_rate', 0),
                'total_pnl': analytics.get('total_pnl', 0),
                'trades_30_days': analytics.get('trades_30_days', 0),
                'wins_30_days': analytics.get('wins_30_days', 0),
                'win_rate_30': analytics.get('win_rate_30', 0),
                'pnl_30_days': analytics.get('pnl_30_days', 0),
                'win_loss_data': win_loss,
                'top_symbols': [dict(s) for s in top_symbols],
                'pnl_by_date': pnl_by_date,
                'daily_stats': daily_stats
            })
        except Exception as e:
            logger.error(f"Analytics error: {e}")
            return jsonify({
                'total_trades': 0,
                'winning_trades': 0,
                'win_rate': 0,
                'total_pnl': 0,
                'trades_30_days': 0,
                'wins_30_days': 0,
                'win_rate_30': 0,
                'pnl_30_days': 0,
                'win_loss_data': {'wins': 0, 'losses': 0, 'breaks': 0},
                'top_symbols': [],
                'pnl_by_date': [],
                'daily_stats': []
            })
    
    @app.route('/api/toggle-auto', methods=['POST'])
    def toggle_auto_trading():
        """Toggle automatic trading on/off"""
        try:
            if auto_engine:
                if auto_engine.is_running:
                    auto_engine.stop()
                    running = False
                else:
                    auto_engine.start()
                    running = True
                
                logger.info(f"🤖 Auto-trading toggled: {'ON' if running else 'OFF'}")
                return jsonify({'running': running, 'status': 'success'})
            else:
                logger.error("Auto engine not initialized")
                return jsonify({'running': False, 'status': 'auto_engine_not_available'})
        except Exception as e:
            logger.error(f"Toggle error: {e}")
            return jsonify({'running': False, 'status': 'error', 'message': str(e)})
    
    @app.route('/api/test-trade', methods=['POST'])
    def test_trade():
        """Run a quick test trade (buy and sell)"""
        try:
            logger.info("🧪 Starting test trade...")
            
            # Get current market data
            market_data = market_fetcher.get_market_data()
            buy_price = market_data['price']
            
            logger.info(f"📊 Current Price: ${buy_price:.2f}")
            
            # Simulate buy
            buy_qty = (1000 * 0.01) / buy_price  # 1% risk of $1000
            buy_cost = buy_qty * buy_price
            
            logger.info(f"🟢 BUY: {buy_qty:.6f} BTC @ ${buy_price:.2f}")
            
            # Simulate sell (0.5% profit)
            sell_price = buy_price * 1.005
            sell_proceeds = buy_qty * sell_price
            profit = sell_proceeds - buy_cost
            profit_pct = (profit / buy_cost) * 100
            
            logger.info(f"🔴 SELL: {buy_qty:.6f} BTC @ ${sell_price:.2f}")
            logger.info(f"💰 Profit: ${profit:.4f} ({profit_pct:.2f}%)")
            logger.info("✅ TEST TRADE COMPLETE")
            
            return jsonify({
                'status': 'success',
                'symbol': TRADING_CONFIG['symbol'],
                'buy_price': buy_price,
                'sell_price': sell_price,
                'quantity': buy_qty,
                'buy_cost': buy_cost,
                'sell_proceeds': sell_proceeds,
                'profit': profit,
                'profit_pct': profit_pct
            })
            
        except Exception as e:
            logger.error(f"Test trade error: {e}")
            return jsonify({
                'status': 'error',
                'error': str(e)
            })
    
    # =====================================================
    # Autonomous AI Trading API Endpoints
    # =====================================================
    
    @app.route('/api/autonomous-status')
    def get_autonomous_status():
        """Get autonomous AI trader status"""
        try:
            if not AUTONOMOUS_MODE or not autonomous_trader:
                return jsonify({
                    'enabled': False,
                    'mode': 'MANUAL',
                    'message': 'Autonomous mode is not enabled'
                })
            
            status = autonomous_trader.get_status()
            return jsonify({
                'enabled': True,
                'mode': 'AUTONOMOUS',
                'is_running': status.get('is_running', False),
                'trades_executed': status.get('trades_executed', 0),
                'last_decision_time': status.get('last_decision_time', 'None'),
                'current_confidence': status.get('current_confidence', 0),
                'active_positions': status.get('active_positions', 0),
                'loop_iterations': status.get('loop_iterations', 0),
                'primary_ai_failures': status.get('primary_ai_failures', 0),
                'backup_service_used': status.get('backup_service_used', None)
            })
        except Exception as e:
            logger.error(f"Autonomous status error: {e}")
            return jsonify({
                'error': str(e),
                'status': 'error'
            }), 500
    
    @app.route('/api/autonomous-history')
    def get_autonomous_history():
        """Get recent autonomous AI trading decisions"""
        try:
            if not AUTONOMOUS_MODE or not autonomous_trader:
                return jsonify({
                    'enabled': False,
                    'decisions': []
                })
            
            history = autonomous_trader.get_execution_history()
            return jsonify({
                'enabled': True,
                'total_decisions': len(history),
                'recent_decisions': history[-20:],  # Last 20 decisions
                'decisions': history
            })
        except Exception as e:
            logger.error(f"Autonomous history error: {e}")
            return jsonify({
                'error': str(e),
                'decisions': [],
                'status': 'error'
            }), 500
    
    @app.route('/api/backup-services-status')
    def get_backup_services_status():
        """Get status of backup AI services"""
        try:
            if not AUTONOMOUS_MODE or not autonomous_trader:
                return jsonify({
                    'enabled': False,
                    'services': []
                })
            
            services_status = autonomous_trader.backup_service.get_status()
            return jsonify({
                'enabled': ENABLE_BACKUP_APIS,
                'services': services_status.get('services', []),
                'total_services': services_status.get('total_services', 0),
                'active_services': services_status.get('active_services', 0),
                'status': services_status
            })
        except Exception as e:
            logger.error(f"Backup services status error: {e}")
            return jsonify({
                'error': str(e),
                'enabled': ENABLE_BACKUP_APIS,
                'services': []
            }), 500
    
    @app.route('/api/autonomous-toggle', methods=['POST'])
    def toggle_autonomous_mode():
        """Start or stop autonomous trading"""
        try:
            if not AUTONOMOUS_MODE or not autonomous_trader:
                return jsonify({
                    'status': 'error',
                    'message': 'Autonomous mode not enabled',
                    'running': False
                })
            
            status = autonomous_trader.get_status()
            
            if status.get('is_running', False):
                autonomous_trader.stop()
                logger.info("🛑 Autonomous trader STOPPED")
                running = False
            else:
                autonomous_trader.start()
                logger.info("🚀 Autonomous trader STARTED")
                running = True
            
            return jsonify({
                'status': 'success',
                'running': running,
                'message': f'Autonomous trader {"STARTED" if running else "STOPPED"}'
            })
        except Exception as e:
            logger.error(f"Toggle autonomous error: {e}")
            return jsonify({
                'status': 'error',
                'error': str(e),
                'running': False
            }), 500
    
    # Log startup info
    logger.info("")
    logger.info("✅ All services initialized successfully!")
    logger.info(f"📈 Starting web dashboard on http://{FLASK_HOST}:{FLASK_PORT}")
    logger.info("🌐 Open your browser and navigate to http://localhost:5000")
    
    if AUTONOMOUS_MODE:
        logger.info("")
        logger.info("🤖 AUTONOMOUS AI TRADER ENABLED")
        logger.info("📊 Available API Endpoints:")
        logger.info("   • GET  /api/autonomous-status        - Current autonomous trader state")
        logger.info("   • GET  /api/autonomous-history       - Recent AI decisions (last 20)")
        logger.info("   • GET  /api/backup-services-status   - Backup AI services health")
        logger.info("   • POST /api/autonomous-toggle        - Start/stop autonomous trader")
    else:
        logger.info("")
        logger.info("🎮 MANUAL TRADING MODE (No autonomous AI)")
    
    logger.info("")
    
    try:
        # Start Flask server
        app.run(
            host=FLASK_HOST,
            port=FLASK_PORT,
            debug=FLASK_DEBUG,
            use_reloader=False
        )
    except KeyboardInterrupt:
        logger.info("\nShutting down...")
        stop_bot()
    except Exception as e:
        logger.error(f"Error running app: {e}")
        stop_bot()


if __name__ == '__main__':
    main()
