/**
 * Analytics Component
 * Displays detailed analytics and statistics
 */

import React, { useRef, useEffect } from 'react';
import { formatCurrency, formatPercent } from '../utils/helpers';

export default function Analytics({ data, loading }) {
    const profitChartRef = useRef(null);
    const winChartRef = useRef(null);

    if (loading) {
        return (
            <div className="card">
                <div className="loading">
                    <div className="spinner"></div>
                    <p style={{ marginTop: '15px' }}>Loading analytics...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="card">
            <h2>📊 Analytics & Statistics</h2>

            {/* Key Metrics */}
            <h3 style={{ marginTop: '20px' }}>Performance Metrics</h3>
            <div className="grid-4">
                <div className="stat-card">
                    <div className="stat-label">Winning Trades</div>
                    <div className="stat-value" style={{ color: '#00ff88' }}>
                        {data.winning_trades}
                    </div>
                </div>
                <div className="stat-card">
                    <div className="stat-label">Losing Trades</div>
                    <div className="stat-value" style={{ color: '#ff4466' }}>
                        {(data.total_trades - data.winning_trades)}
                    </div>
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
            </div>

            {/* Charts */}
            <div className="grid-2" style={{ marginTop: '30px' }}>
                <div>
                    <h3>Win/Loss Distribution</h3>
                    <div className="chart-container">
                        <canvas ref={winChartRef}></canvas>
                    </div>
                </div>
                <div>
                    <h3>Profit/Loss Trend</h3>
                    <div className="chart-container">
                        <canvas ref={profitChartRef}></canvas>
                    </div>
                </div>
            </div>

            {/* Daily Stats */}
            <h3 style={{ marginTop: '30px' }}>Daily Statistics</h3>
            {data.analytics?.daily_stats && data.analytics.daily_stats.length > 0 ? (
                <div className="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Date</th>
                                <th>Trades</th>
                                <th>Winners</th>
                                <th>Losers</th>
                                <th>Win Rate</th>
                                <th>P&L</th>
                            </tr>
                        </thead>
                        <tbody>
                            {data.analytics.daily_stats.map((stat, idx) => (
                                <tr key={idx}>
                                    <td>{new Date(stat.date).toLocaleDateString()}</td>
                                    <td>{stat.total_trades}</td>
                                    <td style={{ color: '#00ff88' }}>{stat.winning_trades}</td>
                                    <td style={{ color: '#ff4466' }}>{stat.losing_trades}</td>
                                    <td>{formatPercent(stat.win_rate)}</td>
                                    <td className={stat.daily_pnl >= 0 ? 'text-success' : 'text-danger'}>
                                        {formatCurrency(stat.daily_pnl)}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            ) : (
                <div className="empty-state">
                    <p>No analytics data available</p>
                </div>
            )}
        </div>
    );
}
