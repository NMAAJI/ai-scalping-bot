/**
 * Journal Component
 * Displays detailed trade journal and history
 */

import React from 'react';
import { formatCurrency, formatDate } from '../utils/helpers';

export default function Journal({ data, loading }) {
    if (loading) {
        return (
            <div className="card">
                <div className="loading">
                    <div className="spinner"></div>
                    <p style={{ marginTop: '15px' }}>Loading journal...</p>
                </div>
            </div>
        );
    }

    const trades = data?.trade_history || [];

    return (
        <div className="card">
            <h2>📓 Trade Journal</h2>

            {trades.length > 0 ? (
                <div className="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Timestamp</th>
                                <th>Symbol</th>
                                <th>Type</th>
                                <th>Entry Price</th>
                                <th>Exit Price</th>
                                <th>Quantity</th>
                                <th>P&L</th>
                                <th>Return %</th>
                                <th>Status</th>
                                <th>Duration</th>
                            </tr>
                        </thead>
                        <tbody>
                            {trades.map((trade, idx) => {
                                const entryPrice = Number(trade.entry_price) || 0;
                                const exitPrice = Number(trade.exit_price) || 0;
                                const quantity = Number(trade.quantity) || 0;

                                const pnl = exitPrice ? (exitPrice - entryPrice) * quantity : 0;
                                const returnPct = entryPrice ? (pnl / (entryPrice * quantity)) * 100 : 0;
                                const duration = trade.exit_time && trade.entry_time
                                    ? Math.round((new Date(trade.exit_time) - new Date(trade.entry_time)) / 60000) 
                                    : null;

                                return (
                                    <tr key={trade.id || idx}>
                                        <td>{formatDate(trade.entry_time)}</td>
                                        <td style={{ color: '#00d4ff' }}>{trade.symbol}</td>
                                        <td>
                                            <span className={`table-status ${trade.type?.toLowerCase()}`}>
                                                {trade.type}
                                            </span>
                                        </td>
                                        <td>{formatCurrency(entryPrice)}</td>
                                        <td>{exitPrice ? formatCurrency(exitPrice) : 'N/A'}</td>
                                        <td>{quantity.toFixed(6)}</td>
                                        <td className={pnl >= 0 ? 'text-success' : 'text-danger'}>
                                            {formatCurrency(pnl)}
                                        </td>
                                        <td className={returnPct >= 0 ? 'text-success' : 'text-danger'}>
                                            {returnPct.toFixed(2)}%
                                        </td>
                                        <td>
                                            <span style={{ 
                                                color: trade.status === 'CLOSED' ? '#00ff88' : '#ffaa00',
                                                fontWeight: 'bold'
                                            }}>
                                                {trade.status}
                                            </span>
                                        </td>
                                        <td>{duration !== null ? `${duration} min` : 'Open'}</td>
                                    </tr>
                                );
                            })}
                        </tbody>
                    </table>
                </div>
            ) : (
                <div className="empty-state">
                    <div className="empty-icon">📭</div>
                    <p>No trades in journal yet</p>
                </div>
            )}
        </div>
    );
}
