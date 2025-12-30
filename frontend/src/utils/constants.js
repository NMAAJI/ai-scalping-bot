/**
 * Constants
 * Global constants and configuration
 */

export const REFRESH_INTERVAL = 3000; // 3 seconds
export const CHART_COLORS = {
    primary: '#00d4ff',
    success: '#00ff88',
    danger: '#ff4466',
    warning: '#ffaa00',
    dark: '#0a0e27',
    darkAlt: '#1a1f3a',
    text: '#fff',
    textMuted: '#8b92b0'
};

export const TAB_NAMES = {
    OVERVIEW: 'overview',
    CHART: 'chart',
    ANALYTICS: 'analytics',
    JOURNAL: 'journal',
    PERFORMANCE: 'performance'
};

export const API_ENDPOINTS = {
    STATUS: '/api/status',
    ANALYTICS: '/api/analytics',
    TRADE_HISTORY: '/api/trade-history',
    TOGGLE_AUTO: '/api/toggle-auto',
    MARKET_DATA: '/api/market-data',
    PERFORMANCE: '/api/performance'
};

export const TRADE_TYPES = {
    BUY: 'BUY',
    SELL: 'SELL',
    HOLD: 'HOLD'
};

export const DEFAULT_STATE = {
    bot_running: false,
    price: 0,
    active_positions: 0,
    total_trades: 0,
    winning_trades: 0,
    win_rate: 0,
    total_pnl: 0,
    today_pnl: 0,
    avg_profit: 0,
    avg_loss: 0,
    positions: [],
    recent_trades: [],
    trade_history: [],
    analytics: {},
    market_data: {},
    performance_metrics: {}
};

export const CHART_CONFIG = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            labels: {
                color: CHART_COLORS.textMuted,
                font: {
                    size: 12
                }
            }
        }
    },
    scales: {
        x: {
            ticks: {
                color: CHART_COLORS.textMuted
            },
            grid: {
                color: 'rgba(139, 146, 176, 0.1)'
            }
        },
        y: {
            ticks: {
                color: CHART_COLORS.textMuted
            },
            grid: {
                color: 'rgba(139, 146, 176, 0.1)'
            }
        }
    }
};
