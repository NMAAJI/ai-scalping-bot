/**
 * Overview Component
 * Displays main statistics and status
 */

import React from 'react';
import { formatCurrency, formatPercent } from '../utils/helpers';

export default function Overview({ data, loading, onToggleAutoTrading }) {
    if (loading) {
        return (
            <div className="card">
                <div className="loading">
                    <div className="spinner"></div>
                    <p style={{ marginTop: '15px' }}>Loading dashboard...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="card">
            {/* Status */}
            <div className="status-card">
                <div className="status-content">
                    <div>
                        <h3>Bot Status</h3>
                        <p style={{ color: '#8b92b0' }}>
                            {data.bot_running ? '🟢 Running' : '🔴 Stopped'}
                            <span className={`status-indicator ${data.bot_running ? 'running' : 'stopped'}`} style={{ marginLeft: '10px' }}></span>
                        </p>
                    </div>
                </div>
                <button
                    className={`btn ${data.bot_running ? 'btn-danger' : 'btn-success'}`}
                    onClick={onToggleAutoTrading}
                >
                    {data.bot_running ? '⏸ STOP' : '▶ START'}
                </button>
            </div>

            {/* Key Stats */}
            <div className="stats-grid">
                <div className="stat-card">
                    <div className="stat-label">Current Price</div>
                    <div className="stat-value">{formatCurrency(data.price)}</div>
                </div>
                <div className="stat-card">
                    <div className="stat-label">Active Positions</div>
                    <div className="stat-value">{data.active_positions}</div>
                </div>
                <div className="stat-card">
                    <div className="stat-label">Total Trades</div>
                    <div className="stat-value">{data.total_trades}</div>
                </div>
                <div className="stat-card">
                    <div className="stat-label">Win Rate</div>
                    <div className={`stat-value ${data.win_rate >= 50 ? 'profit' : 'loss'}`}>
                        {formatPercent(data.win_rate)}
                    </div>
                </div>
                <div className="stat-card">
                    <div className="stat-label">Total P&L</div>
                    <div className={`stat-value ${data.total_pnl >= 0 ? 'profit' : 'loss'}`}>
                        {formatCurrency(data.total_pnl)}
                    </div>
                </div>
                <div className="stat-card">
                    <div className="stat-label">Today P&L</div>
                    <div className={`stat-value ${data.today_pnl >= 0 ? 'profit' : 'loss'}`}>
                        {formatCurrency(data.today_pnl)}
                    </div>
                </div>
                <div className="stat-card">
                    <div className="stat-label">Avg Profit</div>
                    <div className="stat-value profit">{formatPercent(data.avg_profit)}</div>
                </div>
                <div className="stat-card">
                    <div className="stat-label">Avg Loss</div>
                    <div className="stat-value loss">{formatPercent(data.avg_loss)}</div>
                </div>
            </div>

            {/* Recent Trades */}
            <h3>Recent Trades</h3>
            {data.recent_trades && data.recent_trades.length > 0 ? (
                <div className="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Timestamp</th>
                                <th>Type</th>
                                <th>Price</th>
                                <th>Quantity</th>
                                <th>P&L</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            {data.recent_trades.map((trade, idx) => (
                                <tr key={idx}>
                                    <td>{new Date(trade.timestamp).toLocaleString()}</td>
                                    <td>
                                        <span className={`table-status ${trade.type.toLowerCase()}`}>
                                            {trade.type}
                                        </span>
                                    </td>
                                    <td>{formatCurrency(trade.price)}</td>
                                    <td>{trade.quantity.toFixed(4)}</td>
                                    <td className={trade.pnl >= 0 ? 'text-success' : 'text-danger'}>
                                        {formatCurrency(trade.pnl)}
                                    </td>
                                    <td>{trade.status}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            ) : (
                <div className="empty-state">
                    <div className="empty-icon">📭</div>
                    <p>No trades yet</p>
                </div>
            )}
        </div>
    );
}
