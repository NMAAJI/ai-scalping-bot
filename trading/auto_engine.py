"""
Automated Trading Engine
Fully automatic buy/sell based on AI rules and risk management
"""

import logging
import time
from datetime import datetime
from typing import Dict, Optional
from config.settings import TRADING_CONFIG

logger = logging.getLogger(__name__)


class AutoTradingEngine:
    """Automated trading execution engine"""
    
    def __init__(self, data_fetcher, ai_analyzer, trade_executor):
        """
        Initialize auto trading engine
        
        Args:
            data_fetcher: Market data fetcher
            ai_analyzer: AI analyzer for predictions
            trade_executor: Trade executor
        """
        self.data_fetcher = data_fetcher
        self.ai_analyzer = ai_analyzer
        self.trade_executor = trade_executor
        self.is_running = False
        self.last_trade_time = None
        self.trades_today = 0
        self.loss_today = 0
    
    def calculate_ai_score(self, market_data: Dict) -> float:
        """
        Calculate AI trading score (0-100)
        
        Score = (Trend×30 + Volume×25 + Sentiment×15 + RR×20 + News×10) / 100
        
        Args:
            market_data: Market data from fetcher
            
        Returns:
            AI score (0-100)
        """
        try:
            score = 0
            
            # 1. Trend Strength (0-30)
            ema_fast = market_data.get('ema_fast', 0)
            ema_slow = market_data.get('ema_slow', 0)
            current_price = market_data.get('current_price', 0)
            
            if ema_fast > ema_slow and current_price > ema_slow:
                trend_score = 30  # Strong bullish
            elif ema_fast < ema_slow and current_price < ema_slow:
                trend_score = 25  # Strong bearish
            else:
                trend_score = 10  # Weak signal
            
            # 2. Volume (0-25)
            avg_volume = market_data.get('avg_volume', 1)
            current_volume = market_data.get('volume', 1)
            volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1
            
            if volume_ratio > 1.5:
                volume_score = 25
            elif volume_ratio > 1.2:
                volume_score = 20
            elif volume_ratio > 1.0:
                volume_score = 15
            else:
                volume_score = 5
            
            # 3. Market Sentiment (0-15)
            rsi = market_data.get('rsi', 50)
            
            if 30 < rsi < 70:
                sentiment_score = 15  # Healthy range
            elif rsi < 30 or rsi > 70:
                sentiment_score = 10  # Extreme (caution)
            else:
                sentiment_score = 5  # Neutral
            
            # 4. Risk:Reward (0-20) - Assume good setup
            rr_ratio = market_data.get('rr_ratio', 1.5)
            
            if rr_ratio >= 2.5:
                rr_score = 20
            elif rr_ratio >= 2.0:
                rr_score = 18
            elif rr_ratio >= 1.5:
                rr_score = 15
            elif rr_ratio >= 1.0:
                rr_score = 10
            else:
                rr_score = 0
            
            # 5. News Risk (0-10)
            has_major_event = market_data.get('has_major_event', False)
            news_score = 0 if has_major_event else 10
            
            # Total AI Score
            total_score = trend_score + volume_score + sentiment_score + rr_score + news_score
            
            logger.info(f"AI Score: {total_score}/100 (Trend:{trend_score} Vol:{volume_score} Sent:{sentiment_score} RR:{rr_score} News:{news_score})")
            
            return min(total_score, 100)
        
        except Exception as e:
            logger.error(f"AI score calculation error: {e}")
            return 0
    
    def check_risk_management(self) -> bool:
        """
        Check if we can trade based on risk management rules
        
        Returns:
            True if safe to trade, False if limits exceeded
        """
        try:
            # Check daily loss limit (2%)
            capital = TRADING_CONFIG.get('capital', 10000)
            daily_loss_limit = capital * 0.02  # 2% max daily loss
            
            if self.loss_today > daily_loss_limit:
                logger.warning(f"⛔ Daily loss limit exceeded: ${self.loss_today:.2f} > ${daily_loss_limit:.2f}")
                return False
            
            # Check max trades per day (3 trades)
            max_trades_per_day = TRADING_CONFIG.get('max_trades_per_day', 3)
            
            if self.trades_today >= max_trades_per_day:
                logger.warning(f"⛔ Max trades per day reached: {self.trades_today} >= {max_trades_per_day}")
                return False
            
            # Check min time between trades (5 minutes)
            if self.last_trade_time:
                time_since_trade = (datetime.now() - self.last_trade_time).total_seconds() / 60
                if time_since_trade < 5:
                    logger.debug(f"⏳ Waiting between trades: {time_since_trade:.1f}m")
                    return False
            
            return True
        
        except Exception as e:
            logger.error(f"Risk check error: {e}")
            return False
    
    def generate_trade_signal(self, market_data: Dict) -> Optional[Dict]:
        """
        Generate trading signal based on analysis
        
        Args:
            market_data: Market data
            
        Returns:
            Trade signal or None
        """
        try:
            ai_score = self.calculate_ai_score(market_data)
            
            # Need score >= 70 to trade
            if ai_score < 70:
                logger.debug(f"📊 AI Score {ai_score}/100 - Below threshold (need 70+)")
                return None
            
            # Determine trade direction
            ema_fast = market_data.get('ema_fast', 0)
            ema_slow = market_data.get('ema_slow', 0)
            current_price = market_data.get('current_price', 0)
            
            if ema_fast > ema_slow and current_price > ema_slow:
                trade_type = 'BUY'
                probability = 0.65
            elif ema_fast < ema_slow and current_price < ema_slow:
                trade_type = 'SELL'
                probability = 0.60
            else:
                logger.debug("No clear trend direction")
                return None
            
            # Calculate position
            atr = market_data.get('atr', 10)
            stop_loss = current_price - atr if trade_type == 'BUY' else current_price + atr
            take_profit = current_price + (atr * 2) if trade_type == 'BUY' else current_price - (atr * 2)
            
            # Calculate position size (1% risk)
            capital = TRADING_CONFIG.get('capital', 10000)
            risk_amount = capital * TRADING_CONFIG.get('risk_per_trade', 0.01)
            price_risk = abs(current_price - stop_loss)
            quantity = risk_amount / price_risk if price_risk > 0 else 0
            
            signal = {
                'type': trade_type,
                'symbol': TRADING_CONFIG.get('symbol', 'BTCUSDT'),
                'entry_price': current_price,
                'stop_loss': stop_loss,
                'take_profit': take_profit,
                'quantity': quantity,
                'ai_score': ai_score,
                'probability': probability,
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"🎯 Trade Signal: {trade_type} @ ${current_price:.2f} (AI:{ai_score} Prob:{probability*100:.0f}%)")
            return signal
        
        except Exception as e:
            logger.error(f"Signal generation error: {e}")
            return None
    
    def execute_trade_auto(self, signal: Dict) -> bool:
        """
        Automatically execute trade
        
        Args:
            signal: Trade signal
            
        Returns:
            True if trade executed, False otherwise
        """
        try:
            # Check risk management first
            if not self.check_risk_management():
                logger.warning("❌ Risk management check failed - trade blocked")
                return False
            
            # Execute trade
            logger.info(f"💰 Executing: {signal['type']} {signal['quantity']:.4f} @ ${signal['entry_price']:.2f}")
            
            # Add to trade executor queue (will execute)
            if not hasattr(self.trade_executor, 'pending_signals'):
                self.trade_executor.pending_signals = []
            
            self.trade_executor.pending_signals.append(signal)
            
            # Update tracking
            self.last_trade_time = datetime.now()
            self.trades_today += 1
            
            logger.info(f"✅ Trade queued for execution (Today: {self.trades_today} trades)")
            return True
        
        except Exception as e:
            logger.error(f"Trade execution error: {e}")
            return False
    
    def monitor_market(self) -> None:
        """
        Continuously monitor market and execute trades automatically
        """
        logger.info("🤖 Auto-Trading Engine Started")
        self.is_running = True
        
        while self.is_running:
            try:
                # Fetch market data
                market_data = self.data_fetcher.get_market_data()
                
                if not market_data:
                    logger.debug("No market data")
                    time.sleep(TRADING_CONFIG.get('check_interval', 60))
                    continue
                
                # Generate signal
                signal = self.generate_trade_signal(market_data)
                
                if signal:
                    # Execute trade
                    self.execute_trade_auto(signal)
                
                # Sleep before next check
                time.sleep(TRADING_CONFIG.get('check_interval', 60))
            
            except Exception as e:
                logger.error(f"Market monitoring error: {e}")
                time.sleep(TRADING_CONFIG.get('check_interval', 60))
    
    def start(self) -> None:
        """Start automatic trading"""
        if not self.is_running:
            logger.info("🟢 Starting Automatic Trading")
            self.is_running = True
            # Monitoring happens in separate thread
    
    def stop(self) -> None:
        """Stop automatic trading"""
        if self.is_running:
            logger.info("🔴 Stopping Automatic Trading")
            self.is_running = False
    
    def reset_daily_stats(self) -> None:
        """Reset daily statistics at midnight"""
        self.trades_today = 0
        self.loss_today = 0
        logger.info("📊 Daily stats reset")
