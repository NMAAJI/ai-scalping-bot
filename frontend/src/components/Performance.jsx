/**
 * Performance Component
 * Displays detailed performance metrics and goals
 */

import React from 'react';
import { formatCurrency, formatPercent } from '../utils/helpers';

export default function Performance({ data, loading }) {
    if (loading) {
        return (
            <div className="card">
                <div className="loading">
                    <div className="spinner"></div>
                    <p style={{ marginTop: '15px' }}>Loading performance...</p>
                </div>
            </div>
        );
    }

    const metrics = data.performance_metrics || {};

    return (
        <div className="card">
            <h2>🏆 Performance Analysis</h2>

            {/* Key Performance Metrics */}
            <h3 style={{ marginTop: '20px' }}>Key Metrics</h3>
            <div className="grid-4">
                <div className="stat-card">
                    <div className="stat-label">Sharpe Ratio</div>
                    <div className="stat-value">
                        {metrics.sharpe_ratio ? metrics.sharpe_ratio.toFixed(2) : 'N/A'}
                    </div>
                </div>
                <div className="stat-card">
                    <div className="stat-label">Max Drawdown</div>
                    <div className="stat-value loss">
                        {metrics.max_drawdown ? formatPercent(metrics.max_drawdown) : 'N/A'}
                    </div>
                </div>
                <div className="stat-card">
                    <div className="stat-label">Profit Factor</div>
                    <div className="stat-value">
                        {metrics.profit_factor ? metrics.profit_factor.toFixed(2) : 'N/A'}
                    </div>
                </div>
                <div className="stat-card">
                    <div className="stat-label">ROI</div>
                    <div className={`stat-value ${metrics.roi >= 0 ? 'profit' : 'loss'}`}>
                        {metrics.roi ? formatPercent(metrics.roi) : 'N/A'}
                    </div>
                </div>
            </div>

            {/* Monthly Performance */}
            <h3 style={{ marginTop: '30px' }}>Monthly Performance</h3>
            {metrics.monthly_stats && metrics.monthly_stats.length > 0 ? (
                <div className="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Month</th>
                                <th>Trades</th>
                                <th>Win Rate</th>
                                <th>Total P&L</th>
                                <th>Avg P&L/Trade</th>
                                <th>Return %</th>
                            </tr>
                        </thead>
                        <tbody>
                            {metrics.monthly_stats.map((stat, idx) => (
                                <tr key={idx}>
                                    <td>{new Date(stat.month + '-01').toLocaleDateString('en-US', { month: 'long', year: 'numeric' })}</td>
                                    <td>{stat.total_trades}</td>
                                    <td>{formatPercent(stat.win_rate)}</td>
                                    <td className={stat.monthly_pnl >= 0 ? 'text-success' : 'text-danger'}>
                                        {formatCurrency(stat.monthly_pnl)}
                                    </td>
                                    <td className={stat.avg_pnl >= 0 ? 'text-success' : 'text-danger'}>
                                        {formatCurrency(stat.avg_pnl)}
                                    </td>
                                    <td className={stat.monthly_return >= 0 ? 'text-success' : 'text-danger'}>
                                        {formatPercent(stat.monthly_return)}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            ) : (
                <div className="empty-state">
                    <p>No monthly data available yet</p>
                </div>
            )}

            {/* Goals */}
            <h3 style={{ marginTop: '30px' }}>Performance Goals</h3>
            <div className="grid-2">
                <div className="card" style={{ background: 'rgba(0, 255, 136, 0.1)', border: '1px solid rgba(0, 255, 136, 0.3)' }}>
                    <h4 style={{ color: '#00ff88', marginBottom: '10px' }}>💰 Daily Goal</h4>
                    <div className="stat-value" style={{ color: '#00ff88' }}>
                        ${metrics.daily_goal || '100.00'}
                    </div>
                    <p style={{ color: '#8b92b0', marginTop: '10px', fontSize: '12px' }}>
                        Target: Gain at least $100 per trading day
                    </p>
                </div>
                <div className="card" style={{ background: 'rgba(0, 212, 255, 0.1)', border: '1px solid rgba(0, 212, 255, 0.3)' }}>
                    <h4 style={{ color: '#00d4ff', marginBottom: '10px' }}>📈 Monthly Goal</h4>
                    <div className="stat-value" style={{ color: '#00d4ff' }}>
                        {metrics.monthly_goal || '2500.00'} (2.5%)
                    </div>
                    <p style={{ color: '#8b92b0', marginTop: '10px', fontSize: '12px' }}>
                        Target: 2.5% return on capital per month
                    </p>
                </div>
            </div>
        </div>
    );
}
