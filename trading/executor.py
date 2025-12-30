"""
Trading Module
Handles trade execution and position management on Binance
"""

import logging
from typing import Dict, Optional
from binance.client import Client
from binance.enums import SIDE_BUY, SIDE_SELL, ORDER_TYPE_MARKET
from config.settings import TRADING_CONFIG

logger = logging.getLogger(__name__)


class TradeExecutor:
    """Handles trade execution and position management"""
    
    def __init__(self, binance_client: Client):
        """
        Initialize trade executor
        
        Args:
            binance_client: Binance API client instance
        """
        self.client = binance_client
        self.symbol = TRADING_CONFIG['symbol']
        self.active_positions = {}
        self.trade_history = []
        self.auto_engine = None  # Will be set later
        self.current_price = 0
        self.bot_running = False
    
    def execute_trade(self, ai_decision: Dict, market_data: Dict) -> Dict:
        """
        Execute a trade based on AI decision
        
        Args:
            ai_decision: Trading decision from AI
            market_data: Current market data
        
        Returns:
            Execution result dictionary
        """
        try:
            # Check if position already exists
            if self.symbol in self.active_positions:
                logger.info(f"Position already open for {self.symbol}")
                return {"status": "skipped", "reason": "Position exists"}
            
            # Check confidence threshold
            if ai_decision['confidence'] < TRADING_CONFIG['min_confidence']:
                logger.info(f"Low confidence: {ai_decision['confidence']:.2%}")
                return {"status": "skipped", "reason": "Low confidence"}
            
            # Check max positions
            if len(self.active_positions) >= TRADING_CONFIG['max_positions']:
                logger.info("Max positions reached")
                return {"status": "skipped", "reason": "Max positions"}
            
            action = ai_decision['action']
            
            if action == 'HOLD':
                return {"status": "hold"}
            
            # Calculate position size
            position_info = self._calculate_position_size(ai_decision)
            if not position_info:
                return {"status": "error", "reason": "Invalid position size"}
            
            quantity = position_info['quantity']
            
            # Validate stop loss
            if ai_decision['entry_price'] == ai_decision['stop_loss']:
                return {"status": "error", "reason": "Invalid stop loss"}
            
            # Place market order
            order_side = SIDE_BUY if action == 'BUY' else SIDE_SELL
            
            try:
                order = self.client.create_order(
                    symbol=self.symbol,
                    side=order_side,
                    type=ORDER_TYPE_MARKET,
                    quantity=round(quantity, 6)
                )
            except Exception as e:
                logger.error(f"Order placement failed: {e}")
                return {"status": "error", "reason": str(e)}
            
            # Store position
            position = {
                'symbol': self.symbol,
                'action': action,
                'entry_price': ai_decision['entry_price'],
                'stop_loss': ai_decision['stop_loss'],
                'take_profit': ai_decision['take_profit'],
                'quantity': quantity,
                'entry_time': self._get_timestamp(),
                'confidence': ai_decision['confidence'],
                'reasoning': ai_decision['reasoning'],
                'order_id': order['orderId']
            }
            
            self.active_positions[self.symbol] = position
            
            logger.info(
                f"✅ Trade Executed: {action} {quantity:.6f} {self.symbol} "
                f"@ ${ai_decision['entry_price']:.2f}"
            )
            logger.info(
                f"   SL: ${ai_decision['stop_loss']:.2f} | "
                f"TP: ${ai_decision['take_profit']:.2f}"
            )
            
            return {"status": "executed", "position": position}
            
        except Exception as e:
            logger.error(f"Trade execution error: {e}")
            return {"status": "error", "reason": str(e)}
    
    def check_exit_conditions(self) -> None:
        """Check if any positions should be closed"""
        try:
            for symbol, position in list(self.active_positions.items()):
                # Get current price
                ticker = self.client.get_symbol_ticker(symbol=symbol)
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
                    self.close_position(symbol, current_price, exit_reason)
                    
        except Exception as e:
            logger.error(f"Error checking exit conditions: {e}")
    
    def close_position(self, symbol: str, current_price: float, reason: str) -> None:
        """
        Close position and record trade
        
        Args:
            symbol: Trading symbol
            current_price: Current market price
            reason: Reason for closing (stop_loss, take_profit, etc.)
        """
        try:
            if symbol not in self.active_positions:
                return
            
            position = self.active_positions[symbol]
            
            # Calculate P&L
            if position['action'] == 'BUY':
                pnl = (current_price - position['entry_price']) * position['quantity']
            else:
                pnl = (position['entry_price'] - current_price) * position['quantity']
            
            pnl_percentage = (pnl / (position['entry_price'] * position['quantity'])) * 100
            
            # Close position on exchange
            close_side = SIDE_SELL if position['action'] == 'BUY' else SIDE_BUY
            try:
                self.client.create_order(
                    symbol=symbol,
                    side=close_side,
                    type=ORDER_TYPE_MARKET,
                    quantity=position['quantity']
                )
            except Exception as e:
                logger.error(f"Failed to close position: {e}")
            
            # Record trade
            trade = {
                **position,
                'exit_price': current_price,
                'exit_time': self._get_timestamp(),
                'exit_reason': reason,
                'pnl': pnl,
                'pnl_percentage': pnl_percentage
            }
            
            self.trade_history.append(trade)
            del self.active_positions[symbol]
            
            emoji = "🟢" if pnl > 0 else "🔴"
            logger.info(f"{emoji} Position Closed: {symbol} | {reason}")
            logger.info(f"   P&L: ${pnl:.2f} ({pnl_percentage:.2f}%)")
            
        except Exception as e:
            logger.error(f"Error closing position: {e}")
    
    def _calculate_position_size(self, ai_decision: Dict) -> Optional[Dict]:
        """
        Calculate position size based on risk management rules
        
        Args:
            ai_decision: Trading decision with entry and stop loss prices
        
        Returns:
            Dictionary with quantity and risk info, or None on error
        """
        try:
            account = self.client.get_account()
            usdt_balance = float(
                [b for b in account['balances'] if b['asset'] == 'USDT'][0]['free']
            )
            
            risk_amount = usdt_balance * TRADING_CONFIG['risk_per_trade']
            price_risk = abs(ai_decision['entry_price'] - ai_decision['stop_loss'])
            
            if price_risk == 0:
                return None
            
            quantity = risk_amount / price_risk
            
            return {
                'quantity': quantity,
                'risk_amount': risk_amount,
                'account_balance': usdt_balance
            }
            
        except Exception as e:
            logger.error(f"Error calculating position size: {e}")
            return None
    
    @staticmethod
    def _get_timestamp() -> str:
        """Get ISO format timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_statistics(self) -> Dict:
        """Get detailed trading statistics"""
        winning_trades = sum(1 for t in self.trade_history if t.get('pnl', 0) > 0)
        total = len(self.trade_history)
        win_rate = (winning_trades / total * 100) if total > 0 else 0
        total_pnl = sum(t.get('pnl', 0) for t in self.trade_history)
        
        # Calculate average profit and loss
        profits = [t.get('pnl', 0) for t in self.trade_history if t.get('pnl', 0) > 0]
        losses = [t.get('pnl', 0) for t in self.trade_history if t.get('pnl', 0) < 0]
        
        avg_profit = (sum(profits) / len(profits)) if profits else 0
        avg_loss = (sum(losses) / len(losses)) if losses else 0
        
        # Today's P&L
        from datetime import datetime, timedelta
        today = datetime.now().date()
        today_pnl = sum(
            t.get('pnl', 0) for t in self.trade_history 
            if datetime.fromisoformat(t.get('exit_time', '')).date() == today
        )
        
        return {
            'total_trades': total,
            'winning_trades': winning_trades,
            'losing_trades': total - winning_trades,
            'win_rate': win_rate,
            'total_pnl': total_pnl,
            'today_pnl': today_pnl,
            'avg_profit': avg_profit,
            'avg_loss': avg_loss,
            'active_positions': len(self.active_positions)
        }
