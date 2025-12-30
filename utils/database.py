"""
SQLite Database Module
Handles persistent storage of trades, performance metrics, and daily statistics
"""

import sqlite3
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

# Database path
DB_PATH = Path('data/trading.db')


class TradingDatabase:
    """SQLite database for trade management and analytics"""
    
    def __init__(self):
        """Initialize database connection and create tables"""
        DB_PATH.parent.mkdir(exist_ok=True)
        self.db_path = DB_PATH
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Create database tables if they don't exist"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Trades table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS trades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    trade_type TEXT NOT NULL,
                    entry_price REAL NOT NULL,
                    exit_price REAL,
                    stop_loss REAL NOT NULL,
                    take_profit REAL NOT NULL,
                    quantity REAL NOT NULL,
                    entry_time TIMESTAMP NOT NULL,
                    exit_time TIMESTAMP,
                    pnl REAL,
                    pnl_percent REAL,
                    emotion TEXT,
                    quality_score INTEGER,
                    ai_score INTEGER,
                    notes TEXT,
                    status TEXT DEFAULT 'OPEN',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Daily statistics table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS daily_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    trade_date DATE UNIQUE NOT NULL,
                    total_trades INTEGER DEFAULT 0,
                    winning_trades INTEGER DEFAULT 0,
                    losing_trades INTEGER DEFAULT 0,
                    win_rate REAL DEFAULT 0,
                    daily_pnl REAL DEFAULT 0,
                    avg_profit REAL DEFAULT 0,
                    avg_loss REAL DEFAULT 0,
                    best_trade REAL DEFAULT 0,
                    worst_trade REAL DEFAULT 0,
                    largest_win REAL DEFAULT 0,
                    largest_loss REAL DEFAULT 0,
                    profit_factor REAL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Monthly statistics table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS monthly_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    year_month TEXT UNIQUE NOT NULL,
                    total_trades INTEGER DEFAULT 0,
                    winning_trades INTEGER DEFAULT 0,
                    losing_trades INTEGER DEFAULT 0,
                    win_rate REAL DEFAULT 0,
                    monthly_pnl REAL DEFAULT 0,
                    avg_profit REAL DEFAULT 0,
                    avg_loss REAL DEFAULT 0,
                    profit_factor REAL DEFAULT 0,
                    best_day_pnl REAL DEFAULT 0,
                    worst_day_pnl REAL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Performance metrics table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS performance_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metric_date DATE UNIQUE NOT NULL,
                    total_capital REAL DEFAULT 0,
                    account_equity REAL DEFAULT 0,
                    max_drawdown REAL DEFAULT 0,
                    sharpe_ratio REAL DEFAULT 0,
                    profit_factor REAL DEFAULT 0,
                    recovery_factor REAL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
            logger.info("✅ Database initialized successfully")
        except Exception as e:
            logger.error(f"❌ Database initialization error: {e}")
        finally:
            conn.close()
    
    def save_trade(self, trade: Dict) -> bool:
        """Save trade to database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO trades (
                    symbol, trade_type, entry_price, exit_price,
                    stop_loss, take_profit, quantity, entry_time,
                    exit_time, pnl, pnl_percent, emotion, quality_score,
                    ai_score, notes, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                trade.get('symbol'),
                trade.get('trade_type'),
                trade.get('entry_price'),
                trade.get('exit_price'),
                trade.get('stop_loss'),
                trade.get('take_profit'),
                trade.get('quantity'),
                trade.get('entry_time'),
                trade.get('exit_time'),
                trade.get('pnl'),
                trade.get('pnl_percent'),
                trade.get('emotion'),
                trade.get('quality_score'),
                trade.get('ai_score'),
                trade.get('notes'),
                trade.get('status', 'OPEN')
            ))
            
            conn.commit()
            logger.info(f"✅ Trade saved: {trade.get('symbol')} {trade.get('trade_type')}")
            return True
        except Exception as e:
            logger.error(f"❌ Error saving trade: {e}")
            return False
        finally:
            conn.close()
    
    def get_trades(self, days: int = 30) -> List[Dict]:
        """Get trades from last N days"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            date_filter = datetime.now() - timedelta(days=days)
            cursor.execute("""
                SELECT * FROM trades
                WHERE entry_time >= ?
                ORDER BY entry_time DESC
            """, (date_filter,))
            
            trades = [dict(row) for row in cursor.fetchall()]
            return trades
        except Exception as e:
            logger.error(f"❌ Error fetching trades: {e}")
            return []
        finally:
            conn.close()
    
    def get_today_trades(self) -> List[Dict]:
        """Get trades from today"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            today = datetime.now().date()
            cursor.execute("""
                SELECT * FROM trades
                WHERE DATE(entry_time) = ?
                ORDER BY entry_time DESC
            """, (today,))
            
            trades = [dict(row) for row in cursor.fetchall()]
            return trades
        except Exception as e:
            logger.error(f"❌ Error fetching today's trades: {e}")
            return []
        finally:
            conn.close()
    
    def update_trade_exit(self, trade_id: int, exit_price: float, exit_time: str, pnl: float, pnl_percent: float, status: str = 'CLOSED'):
        """Update trade exit information"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE trades
                SET exit_price = ?, exit_time = ?, pnl = ?, pnl_percent = ?, status = ?
                WHERE id = ?
            """, (exit_price, exit_time, pnl, pnl_percent, status, trade_id))
            
            conn.commit()
            logger.info(f"✅ Trade {trade_id} exit updated: P&L ${pnl:.2f}")
            return True
        except Exception as e:
            logger.error(f"❌ Error updating trade: {e}")
            return False
        finally:
            conn.close()
    
    def save_daily_stats(self, stats: Dict) -> bool:
        """Save or update daily statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            trade_date = stats.get('date', datetime.now().date())
            
            cursor.execute("""
                INSERT OR REPLACE INTO daily_stats (
                    trade_date, total_trades, winning_trades, losing_trades,
                    win_rate, daily_pnl, avg_profit, avg_loss, best_trade,
                    worst_trade, largest_win, largest_loss, profit_factor
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                trade_date,
                stats.get('total_trades', 0),
                stats.get('winning_trades', 0),
                stats.get('losing_trades', 0),
                stats.get('win_rate', 0),
                stats.get('daily_pnl', 0),
                stats.get('avg_profit', 0),
                stats.get('avg_loss', 0),
                stats.get('best_trade', 0),
                stats.get('worst_trade', 0),
                stats.get('largest_win', 0),
                stats.get('largest_loss', 0),
                stats.get('profit_factor', 0)
            ))
            
            conn.commit()
            logger.info(f"✅ Daily stats saved for {trade_date}")
            return True
        except Exception as e:
            logger.error(f"❌ Error saving daily stats: {e}")
            return False
        finally:
            conn.close()
    
    def get_daily_stats(self, days: int = 30) -> List[Dict]:
        """Get daily statistics for last N days"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            date_filter = datetime.now().date() - timedelta(days=days)
            cursor.execute("""
                SELECT * FROM daily_stats
                WHERE trade_date >= ?
                ORDER BY trade_date DESC
            """, (date_filter,))
            
            stats = [dict(row) for row in cursor.fetchall()]
            return stats
        except Exception as e:
            logger.error(f"❌ Error fetching daily stats: {e}")
            return []
        finally:
            conn.close()
    
    def get_monthly_stats(self, months: int = 12) -> List[Dict]:
        """Get monthly statistics for last N months"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT * FROM monthly_stats
                ORDER BY year_month DESC
                LIMIT ?
            """, (months,))
            
            stats = [dict(row) for row in cursor.fetchall()]
            return stats
        except Exception as e:
            logger.error(f"❌ Error fetching monthly stats: {e}")
            return []
        finally:
            conn.close()
    
    def calculate_and_save_daily_stats(self):
        """Calculate and save daily statistics from trades"""
        trades = self.get_today_trades()
        
        if not trades:
            return
        
        wins = [t for t in trades if t.get('pnl', 0) > 0]
        losses = [t for t in trades if t.get('pnl', 0) < 0]
        
        total_pnl = sum(t.get('pnl', 0) for t in trades)
        total_wins = sum(t.get('pnl', 0) for t in wins) if wins else 0
        total_losses = abs(sum(t.get('pnl', 0) for t in losses)) if losses else 0
        
        stats = {
            'date': datetime.now().date(),
            'total_trades': len(trades),
            'winning_trades': len(wins),
            'losing_trades': len(losses),
            'win_rate': (len(wins) / len(trades) * 100) if trades else 0,
            'daily_pnl': total_pnl,
            'avg_profit': (total_wins / len(wins)) if wins else 0,
            'avg_loss': (total_losses / len(losses)) if losses else 0,
            'best_trade': max([t.get('pnl', 0) for t in trades]),
            'worst_trade': min([t.get('pnl', 0) for t in trades]),
            'largest_win': max([t.get('pnl', 0) for t in wins]) if wins else 0,
            'largest_loss': abs(min([t.get('pnl', 0) for t in losses])) if losses else 0,
            'profit_factor': (total_wins / total_losses) if total_losses > 0 else 0
        }
        
        self.save_daily_stats(stats)
        logger.info(f"✅ Daily stats calculated: {stats['win_rate']:.1f}% win rate")
    
    def get_analytics_data(self) -> Dict:
        """Get comprehensive analytics data"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Total stats
            cursor.execute("SELECT COUNT(*) as total FROM trades WHERE status='CLOSED'")
            total_trades = cursor.fetchone()['total']
            
            cursor.execute("SELECT COUNT(*) as wins FROM trades WHERE pnl > 0 AND status='CLOSED'")
            winning_trades = cursor.fetchone()['wins']
            
            cursor.execute("SELECT SUM(pnl) as total_pnl FROM trades WHERE status='CLOSED'")
            total_pnl = cursor.fetchone()['total_pnl'] or 0
            
            # 30-day stats
            date_30 = datetime.now().date() - timedelta(days=30)
            cursor.execute("""
                SELECT COUNT(*) as trades_30,
                       SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) as wins_30,
                       SUM(pnl) as pnl_30
                FROM trades
                WHERE DATE(entry_time) >= ? AND status='CLOSED'
            """, (date_30,))
            
            result_30 = cursor.fetchone()
            trades_30 = result_30['trades_30'] or 0
            wins_30 = result_30['wins_30'] or 0
            pnl_30 = result_30['pnl_30'] or 0
            
            return {
                'total_trades': total_trades,
                'winning_trades': winning_trades,
                'win_rate': (winning_trades / total_trades * 100) if total_trades > 0 else 0,
                'total_pnl': total_pnl,
                'trades_30_days': trades_30,
                'wins_30_days': wins_30,
                'win_rate_30': (wins_30 / trades_30 * 100) if trades_30 > 0 else 0,
                'pnl_30_days': pnl_30
            }
        except Exception as e:
            logger.error(f"❌ Error getting analytics data: {e}")
            return {}
        finally:
            conn.close()
    
    def get_pnl_by_date(self, days: int = 30) -> List[Dict]:
        """Get P&L by date for chart"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            date_filter = datetime.now().date() - timedelta(days=days)
            cursor.execute("""
                SELECT trade_date, daily_pnl, win_rate, total_trades
                FROM daily_stats
                WHERE trade_date >= ?
                ORDER BY trade_date ASC
            """, (date_filter,))
            
            data = [dict(row) for row in cursor.fetchall()]
            return data
        except Exception as e:
            logger.error(f"❌ Error getting P&L data: {e}")
            return []
        finally:
            conn.close()
    
    def get_win_loss_breakdown(self) -> Dict:
        """Get win/loss breakdown for pie chart"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT 
                    SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) as wins,
                    SUM(CASE WHEN pnl < 0 THEN 1 ELSE 0 END) as losses,
                    SUM(CASE WHEN pnl = 0 THEN 1 ELSE 0 END) as breaks
                FROM trades
                WHERE status='CLOSED'
            """)
            
            result = cursor.fetchone()
            return {
                'wins': result['wins'] or 0,
                'losses': result['losses'] or 0,
                'breaks': result['breaks'] or 0
            }
        except Exception as e:
            logger.error(f"❌ Error getting win/loss breakdown: {e}")
            return {'wins': 0, 'losses': 0, 'breaks': 0}
        finally:
            conn.close()
    
    def get_top_performing_symbols(self, limit: int = 5) -> List[Dict]:
        """Get top performing trading symbols"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT symbol,
                       COUNT(*) as trades,
                       SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) as wins,
                       SUM(pnl) as total_pnl,
                       AVG(pnl) as avg_pnl
                FROM trades
                WHERE status='CLOSED'
                GROUP BY symbol
                ORDER BY total_pnl DESC
                LIMIT ?
            """, (limit,))
            
            data = [dict(row) for row in cursor.fetchall()]
            return data
        except Exception as e:
            logger.error(f"❌ Error getting top symbols: {e}")
            return []
        finally:
            conn.close()
