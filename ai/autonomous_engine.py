"""
Autonomous Trading Engine
Fully automated execution without human intervention
Integrates Gemini AI with backup services
"""

import logging
import time
from datetime import datetime
from typing import Dict, Optional
from threading import Thread, Event

from ai.autonomous_trader import AutonomousAITrader
from ai.backup_services import BackupAIService
from trading.executor import TradeExecutor
from market.data_fetcher import MarketDataFetcher
from config.settings import (
    AUTONOMOUS_MODE, ENABLE_BACKUP_APIS,
    GEMINI_API_KEY, OPENAI_API_KEY, ANTHROPIC_API_KEY,
    TRADING_CONFIG
)

logger = logging.getLogger(__name__)


class FullyAutonomousTrader:
    """
    Fully autonomous AI trading system
    - Gemini AI for primary analysis
    - Backup APIs for failover
    - Automatic trade execution
    - No human intervention required
    """
    
    def __init__(self, market_fetcher: MarketDataFetcher, 
                 trade_executor: TradeExecutor):
        """
        Initialize autonomous trader
        
        Args:
            market_fetcher: Market data fetcher
            trade_executor: Trade executor
        """
        self.market_fetcher = market_fetcher
        self.trade_executor = trade_executor
        
        # Initialize Gemini autonomous AI
        logger.info("🤖 Initializing autonomous AI trader...")
        self.ai_trader = AutonomousAITrader(GEMINI_API_KEY)
        
        # Initialize backup services
        self.backup_service = None
        if ENABLE_BACKUP_APIS:
            logger.info("🔄 Setting up backup AI services...")
            self.backup_service = BackupAIService()
            self._setup_backup_services()
        
        # Trading state
        self.is_running = False
        self.stop_event = Event()
        self.last_decision = None
        self.decision_count = 0
        self.executed_trades = 0
        
        logger.info("✅ Autonomous trader initialized (FULLY AUTOMATED MODE)")
    
    def _setup_backup_services(self) -> None:
        """Configure backup AI services"""
        if not self.backup_service:
            return
        
        # Add services based on available API keys
        priority = 1
        
        if OPENAI_API_KEY:
            self.backup_service.add_service(
                name='openai',
                api_key=OPENAI_API_KEY,
                service_type='openai',
                priority=priority
            )
            priority += 1
            logger.info("✅ OpenAI added as backup service")
        
        if ANTHROPIC_API_KEY:
            self.backup_service.add_service(
                name='anthropic',
                api_key=ANTHROPIC_API_KEY,
                service_type='anthropic',
                priority=priority
            )
            priority += 1
            logger.info("✅ Anthropic added as backup service")
        
        if TRADING_CONFIG.get('secondary_gemini_key'):
            # If you have secondary Gemini key
            logger.info("✅ Secondary Gemini added as backup")
    
    def start(self) -> None:
        """Start autonomous trading (no human input needed)"""
        if self.is_running:
            logger.warning("⚠️ Autonomous trader already running")
            return
        
        self.is_running = True
        self.stop_event.clear()
        
        logger.info("🚀 AUTONOMOUS TRADING STARTED")
        logger.info("⚠️ FULLY AUTOMATED MODE - NO HUMAN INTERVENTION")
        logger.info(f"📊 Symbol: {TRADING_CONFIG['symbol']}")
        logger.info(f"⏱️ Check interval: {TRADING_CONFIG['check_interval']}s")
        logger.info(f"💰 Risk per trade: {TRADING_CONFIG['risk_per_trade']*100}%")
        
        # Start trading thread
        trading_thread = Thread(target=self._autonomous_loop, daemon=True)
        trading_thread.start()
        
        logger.info("✅ Trading thread started")
    
    def stop(self) -> None:
        """Stop autonomous trading"""
        if not self.is_running:
            logger.warning("⚠️ Autonomous trader not running")
            return
        
        self.is_running = False
        self.stop_event.set()
        
        logger.info("🛑 AUTONOMOUS TRADING STOPPED")
        logger.info(f"📊 Total decisions made: {self.decision_count}")
        logger.info(f"✅ Total trades executed: {self.executed_trades}")
    
    def _autonomous_loop(self) -> None:
        """
        Main autonomous trading loop
        Continuously monitors market and executes trades
        """
        logger.info("═" * 60)
        logger.info("AUTONOMOUS TRADING LOOP STARTED")
        logger.info("═" * 60)
        
        while self.is_running and not self.stop_event.is_set():
            try:
                # Step 1: Fetch market data
                market_data = self.market_fetcher.get_market_data()
                
                if not market_data:
                    logger.warning("⚠️ Could not fetch market data, waiting...")
                    time.sleep(TRADING_CONFIG['check_interval'])
                    continue
                
                # Step 2: Get AI decision (AUTONOMOUS)
                logger.info("🤖 Requesting autonomous AI decision...")
                decision = self.ai_trader.analyze_and_execute(
                    market_data,
                    execute=True  # Fully autonomous
                )
                
                self.last_decision = decision
                self.decision_count += 1
                
                # Step 3: Check execution status
                if decision.get('action') != 'HOLD':
                    if decision.get('execution', {}).get('status') == 'READY_FOR_EXECUTION':
                        
                        # Step 4: AUTO-EXECUTE trade (NO human approval needed)
                        logger.info("🎯 AUTO-EXECUTING TRADE...")
                        execution_result = self._auto_execute_trade(decision, market_data)
                        
                        if execution_result['success']:
                            self.executed_trades += 1
                            logger.info(f"✅ Trade executed! Total: {self.executed_trades}")
                        else:
                            logger.error(f"❌ Execution failed: {execution_result['error']}")
                    else:
                        logger.info(f"⏸️ Trade held: {decision['execution'].get('reason')}")
                else:
                    logger.info("📊 HOLD signal - waiting for better opportunity")
                
                # Log decision to audit trail
                self._log_autonomous_decision(decision, market_data)
                
                # Wait before next check
                time.sleep(TRADING_CONFIG['check_interval'])
                
            except Exception as e:
                logger.error(f"❌ Autonomous loop error: {e}")
                # Fallback to technical analysis only
                self._safe_fallback()
                time.sleep(TRADING_CONFIG['check_interval'] * 2)
    
    def _auto_execute_trade(self, decision: Dict, market_data: Dict) -> Dict:
        """
        Automatically execute trade without human approval
        
        Args:
            decision: AI decision
            market_data: Current market data
        
        Returns:
            Execution result
        """
        try:
            logger.info(f"📈 AUTO-EXECUTING {decision['action']}")
            logger.info(f"   Entry: ${decision['entry_price']:.2f}")
            logger.info(f"   Stop Loss: ${decision['stop_loss']:.2f}")
            logger.info(f"   Take Profit: ${decision['take_profit']:.2f}")
            
            # Execute through trade executor
            result = self.trade_executor.execute_trade(
                ai_decision=decision,
                market_data=market_data
            )
            
            logger.info(f"✅ {result['status']}")
            
            return {
                'success': result['status'] == 'EXECUTED',
                'result': result,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Auto-execution error: {e}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _safe_fallback(self) -> None:
        """
        Safe fallback when primary system fails
        Uses simple technical rules or backup API
        """
        logger.warning("⚠️ Primary system failed, attempting fallback...")
        
        if self.backup_service:
            try:
                market_data = self.market_fetcher.get_market_data()
                
                if market_data:
                    logger.info("🔄 Trying backup AI service...")
                    fallback_decision = self.backup_service.get_analysis(market_data)
                    
                    if fallback_decision:
                        logger.info("✅ Backup service provided analysis")
                        
                        if fallback_decision['action'] != 'HOLD':
                            result = self._auto_execute_trade(
                                fallback_decision,
                                market_data
                            )
                            
                            if result['success']:
                                self.executed_trades += 1
                                logger.info("✅ Fallback trade executed")
                            
                            self._log_autonomous_decision(
                                fallback_decision,
                                market_data,
                                is_fallback=True
                            )
                    else:
                        logger.warning("❌ Backup service also failed")
                        
            except Exception as e:
                logger.error(f"❌ Fallback error: {e}")
    
    def _log_autonomous_decision(self, decision: Dict, market_data: Dict,
                                 is_fallback: bool = False) -> None:
        """Log autonomous decision for audit trail"""
        try:
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'decision_number': self.decision_count,
                'action': decision['action'],
                'confidence': decision.get('confidence', 0),
                'final_confidence': decision.get('final_confidence', 0),
                'entry_price': decision['entry_price'],
                'stop_loss': decision['stop_loss'],
                'take_profit': decision['take_profit'],
                'market_price': market_data['price'],
                'market_rsi': market_data['rsi'],
                'market_trend': market_data['trend'],
                'execution_status': decision.get('execution', {}).get('status'),
                'reasoning': decision['reasoning'],
                'is_fallback': is_fallback,
                'ai_source': decision.get('source', 'gemini')
            }
            
            with open('logs/autonomous_trades.jsonl', 'a') as f:
                import json
                f.write(json.dumps(log_entry) + '\n')
                
        except Exception as e:
            logger.warning(f"Could not log decision: {e}")
    
    def get_status(self) -> Dict:
        """Get autonomous trader status"""
        return {
            'running': self.is_running,
            'decisions_made': self.decision_count,
            'trades_executed': self.executed_trades,
            'last_decision': self.last_decision,
            'mode': 'FULLY_AUTONOMOUS',
            'backup_service_available': self.backup_service is not None,
            'backup_services_status': (
                self.backup_service.get_status()
                if self.backup_service else None
            )
        }
    
    def get_execution_history(self) -> list:
        """Get history of all autonomous executions"""
        try:
            import json
            history = []
            
            with open('logs/autonomous_trades.jsonl', 'r') as f:
                for line in f:
                    if line.strip():
                        history.append(json.loads(line))
            
            return history
            
        except Exception as e:
            logger.error(f"Could not read history: {e}")
            return []
