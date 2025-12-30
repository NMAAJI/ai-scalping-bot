/**
 * Chart Component
 * Displays price chart and technical analysis
 */

import React, { useRef, useEffect } from 'react';

export default function Chart({ data, loading }) {
    const chartRef = useRef(null);

    if (loading) {
        return (
            <div className="card">
                <div className="loading">
                    <div className="spinner"></div>
                    <p style={{ marginTop: '15px' }}>Loading chart...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="card">
            <h2>📈 Price Chart</h2>

            <div className="chart-container">
                <canvas ref={chartRef}></canvas>
            </div>

            {/* Technical Indicators */}
            <h3 style={{ marginTop: '30px' }}>Technical Indicators</h3>
            <div className="grid-3">
                <div className="stat-card">
                    <div className="stat-label">RSI (14)</div>
                    <div className="stat-value">
                        {data.market_data?.rsi ? data.market_data.rsi.toFixed(2) : 'N/A'}
                    </div>
                </div>
                <div className="stat-card">
                    <div className="stat-label">MACD</div>
                    <div className="stat-value">
                        {data.market_data?.macd ? data.market_data.macd.toFixed(4) : 'N/A'}
                    </div>
                </div>
                <div className="stat-card">
                    <div className="stat-label">Volume</div>
                    <div className="stat-value">
                        {data.market_data?.volume ? (data.market_data.volume / 1000000).toFixed(2) : 'N/A'} M
                    </div>
                </div>
            </div>

            {/* Trend */}
            <h3 style={{ marginTop: '30px' }}>Trend Analysis</h3>
            <div className="grid-2">
                <div className="card" style={{ background: 'rgba(0, 255, 136, 0.1)', border: '1px solid rgba(0, 255, 136, 0.3)' }}>
                    <div className="stat-label" style={{ color: '#00ff88' }}>Trend</div>
                    <div className="stat-value" style={{ color: '#00ff88' }}>
                        {data.market_data?.trend || 'N/A'}
                    </div>
                </div>
                <div className="card" style={{ background: 'rgba(0, 212, 255, 0.1)', border: '1px solid rgba(0, 212, 255, 0.3)' }}>
                    <div className="stat-label" style={{ color: '#00d4ff' }}>Signal</div>
                    <div className="stat-value" style={{ color: '#00d4ff' }}>
                        {data.market_data?.signal || 'HOLD'}
                    </div>
                </div>
            </div>
        </div>
    );
}
