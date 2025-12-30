"""
React-based Dashboard Module
Modern real-time trading dashboard with React and WebSocket support
"""

from flask import Flask, render_template_string, jsonify, Blueprint, request
from typing import Dict, List
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

dashboard_bp = Blueprint('dashboard', __name__)

# React App HTML
REACT_DASHBOARD = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Trading Bot - React Dashboard</title>
    <!-- React & ReactDOM -->
    <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <!-- Babel for JSX -->
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <!-- TradingView Chart Widget -->
    <script src="https://s3.tradingview.com/tv.js"></script>
    <!-- Chart.js for analytics -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js"></script>
    
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
            color: #fff; 
            padding: 15px; 
            min-height: 100vh;
        }
        
        #root {
            max-width: 1600px;
            margin: 0 auto;
        }
        
        h1 { 
            text-align: center; 
            margin-bottom: 25px; 
            color: #00d4ff;
            font-size: 32px;
            text-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
        }
        
        h2 {
            color: #00d4ff;
            margin-bottom: 15px;
            border-bottom: 2px solid #00d4ff;
            padding-bottom: 10px;
        }
        
        h3 {
            color: #00d4ff;
            margin-bottom: 10px;
        }
        
        .tab-container {
            display: flex;
            gap: 10px;
            margin-bottom: 25px;
            flex-wrap: wrap;
        }
        
        .tab-button {
            background: linear-gradient(135deg, #1a1f3a 0%, #252b4a 100%);
            color: #8b92b0;
            border: 2px solid #00d4ff;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s;
        }
        
        .tab-button.active {
            background: #00d4ff;
            color: #0a0e27;
        }
        
        .tab-button:hover {
            background: #1a1f3a;
            border-color: #00ff88;
        }
        
        .card {
            background: linear-gradient(135deg, #1a1f3a 0%, #252b4a 100%);
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #2a3155;
            margin-bottom: 20px;
        }
        
        .status { 
            background: linear-gradient(135deg, #1a1f3a 0%, #252b4a 100%);
            padding: 20px; 
            border-radius: 10px; 
            margin-bottom: 20px;
            border-left: 4px solid #00d4ff;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
        }
        
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-left: 10px;
            animation: pulse 2s infinite;
        }
        
        .status-indicator.running { background-color: #00ff88; }
        .status-indicator.stopped { background-color: #ff4466; }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 12px;
            margin-bottom: 20px;
        }
        
        .stat-card {
            background: #0a0e27;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #00d4ff;
            text-align: center;
        }
        
        .stat-label {
            color: #8b92b0;
            font-size: 12px;
            text-transform: uppercase;
            margin-bottom: 8px;
        }
        
        .stat-value {
            font-size: 20px;
            font-weight: bold;
            color: #00d4ff;
        }
        
        .stat-value.profit { color: #00ff88; }
        .stat-value.loss { color: #ff4466; }
        
        .grid-2 {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }
        
        @media (max-width: 1024px) {
            .grid-2 { grid-template-columns: 1fr; }
        }
        
        .empty {
            text-align: center;
            color: #8b92b0;
            padding: 30px;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }
        
        th {
            background: #0a0e27;
            color: #00d4ff;
            padding: 12px;
            text-align: left;
            border-bottom: 2px solid #00d4ff;
        }
        
        td {
            padding: 10px;
            border-bottom: 1px solid #2a3155;
        }
        
        tr:hover {
            background: rgba(0, 212, 255, 0.05);
        }
        
        .chart-container {
            position: relative;
            width: 100%;
            height: 400px;
            margin-top: 20px;
        }
        
        .loading {
            text-align: center;
            color: #8b92b0;
            padding: 20px;
        }
    </style>
</head>
<body>
    <div id="root"></div>
    
    <script type="text/babel">
        const { useState, useEffect, useRef } = React;
        
        // Main App Component
        function App() {
            const [activeTab, setActiveTab] = useState('overview');
            const [data, setData] = useState({
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
                analytics: {}
            });
            
            // Real-time update effect
            useEffect(() => {
                const interval = setInterval(async () => {
                    try {
                        // Fetch status
                        const statusRes = await fetch('/api/status');
                        const statusData = await statusRes.json();
                        
                        // Fetch analytics
                        const analyticsRes = await fetch('/api/analytics');
                        const analyticsData = await analyticsRes.json();
                        
                        // Fetch trade history
                        const historyRes = await fetch('/api/trade-history');
                        const historyData = await historyRes.json();
                        
                        setData(prev => ({
                            ...prev,
                            ...statusData,
                            analytics: analyticsData,
                            trade_history: historyData.trades
                        }));
                    } catch (error) {
                        console.error('Update error:', error);
                    }
                }, 3000); // Update every 3 seconds
                
                return () => clearInterval(interval);
            }, []);
            
            // Handle tab switching
            const switchTab = (tab) => {
                setActiveTab(tab);
            };
            
            // Toggle auto-trading
            const toggleAutoTrading = async () => {
                try {
                    const res = await fetch('/api/toggle-auto', { method: 'POST' });
                    const result = await res.json();
                    setData(prev => ({ ...prev, bot_running: result.running }));
                } catch (error) {
                    console.error('Toggle error:', error);
                }
            };
            
            return (
                <div className="container">
                    <h1>🤖 AI Trading Bot Dashboard</h1>
                    
                    {/* Tab Buttons */}
                    <div className="tab-container">
                        <button className={`tab-button ${activeTab === 'overview' ? 'active' : ''}`} onClick={() => switchTab('overview')}>📊 Overview</button>
                        <button className={`tab-button ${activeTab === 'chart' ? 'active' : ''}`} onClick={() => switchTab('chart')}>📈 Chart</button>
                        <button className={`tab-button ${activeTab === 'analytics' ? 'active' : ''}`} onClick={() => switchTab('analytics')}>📊 Analytics</button>
                        <button className={`tab-button ${activeTab === 'journal' ? 'active' : ''}`} onClick={() => switchTab('journal')}>📔 Journal</button>
                        <button className={`tab-button ${activeTab === 'performance' ? 'active' : ''}`} onClick={() => switchTab('performance')}>🏆 Performance</button>
                    </div>
                    
                    {/* Tab Content */}
                    {activeTab === 'overview' && <OverviewTab data={data} />}
                    {activeTab === 'chart' && <ChartTab data={data} />}
                    {activeTab === 'analytics' && <AnalyticsTab data={data} />}
                    {activeTab === 'journal' && <JournalTab data={data} />}
                    {activeTab === 'performance' && <PerformanceTab data={data} />}
                </div>
            );
        }
        
        // Overview Tab Component
        function OverviewTab({ data }) {
            const [testResult, setTestResult] = useState(null);
            const [testRunning, setTestRunning] = useState(false);
            
            const toggleAutoTrading = async () => {
                try {
                    const res = await fetch('/api/toggle-auto', { method: 'POST' });
                    const result = await res.json();
                } catch (error) {
                    console.error('Toggle error:', error);
                }
            };
            
            const runTestTrade = async () => {
                setTestRunning(true);
                setTestResult(null);
                try {
                    const res = await fetch('/api/test-trade', { method: 'POST' });
                    const result = await res.json();
                    setTestResult(result);
                } catch (error) {
                    console.error('Test error:', error);
                    setTestResult({ error: 'Test failed: ' + error.message });
                }
                setTestRunning(false);
            };
            
            return (
                <div>
                    {/* Status with Start/Stop and Test */}
                    <div className="status">
                        <div>
                            <h2 style={{ margin: 0, border: 'none', padding: 0 }}>
                                {data.bot_running ? '🟢 AUTO-TRADING RUNNING' : '🔴 AUTO-TRADING STOPPED'}
                                <span className={`status-indicator ${data.bot_running ? 'running' : 'stopped'}`}></span>
                            </h2>
                            <p style={{ color: '#8b92b0', fontSize: '12px', marginTop: '5px' }}>
                                {data.bot_running ? 'Bot is automatically buying and selling based on AI signals' : 'Bot is idle - Click button to start'}
                            </p>
                        </div>
                        <div style={{ display: 'flex', gap: '10px' }}>
                            <button 
                                onClick={toggleAutoTrading}
                                style={{
                                    padding: '12px 30px',
                                    fontSize: '16px',
                                    fontWeight: 'bold',
                                    border: 'none',
                                    borderRadius: '5px',
                                    cursor: 'pointer',
                                    background: data.bot_running ? '#ff4466' : '#00ff88',
                                    color: data.bot_running ? '#fff' : '#000',
                                    transition: 'all 0.3s'
                                }}
                            >
                                {data.bot_running ? '⏹️ STOP' : '▶️ START'}
                            </button>
                            <button 
                                onClick={runTestTrade}
                                disabled={testRunning}
                                style={{
                                    padding: '12px 30px',
                                    fontSize: '16px',
                                    fontWeight: 'bold',
                                    border: 'none',
                                    borderRadius: '5px',
                                    cursor: testRunning ? 'not-allowed' : 'pointer',
                                    background: testRunning ? '#888' : '#00d4ff',
                                    color: '#000',
                                    transition: 'all 0.3s',
                                    opacity: testRunning ? 0.6 : 1
                                }}
                            >
                                {testRunning ? '⏳ TESTING...' : '🧪 TEST TRADE'}
                            </button>
                        </div>
                    </div>
                    
                    {/* Test Results */}
                    {testResult && (
                        <div className="card" style={{ marginTop: '20px', borderLeft: `4px solid ${testResult.error ? '#ff4466' : '#00ff88'}` }}>
                            <h2>🧪 Test Trade Results</h2>
                            {testResult.error ? (
                                <div style={{ color: '#ff4466' }}><strong>❌ Error:</strong> {testResult.error}</div>
                            ) : (
                                <div>
                                    <div style={{ marginBottom: '15px' }}>
                                        <strong>BUY Order:</strong> {testResult.symbol} @ ${testResult.buy_price.toFixed(2)}<br/>
                                        Quantity: {testResult.quantity.toFixed(6)} BTC | Cost: ${testResult.buy_cost.toFixed(4)}
                                    </div>
                                    <div style={{ marginBottom: '15px' }}>
                                        <strong>SELL Order:</strong> {testResult.symbol} @ ${testResult.sell_price.toFixed(2)}<br/>
                                        Proceeds: ${testResult.sell_proceeds.toFixed(4)}
                                    </div>
                                    <div style={{ 
                                        padding: '10px', 
                                        background: 'rgba(0, 255, 136, 0.1)', 
                                        borderRadius: '5px',
                                        color: testResult.profit >= 0 ? '#00ff88' : '#ff4466'
                                    }}>
                                        <strong>💰 Net Profit: ${testResult.profit.toFixed(4)} ({testResult.profit_pct.toFixed(2)}%)</strong>
                                    </div>
                                    <div style={{ marginTop: '15px', fontSize: '12px', color: '#8b92b0' }}>
                                        ✅ All systems verified and ready for live trading!
                                    </div>
                                </div>
                            )}
                        </div>
                    )}
                    
                    {/* Statistics */}
                    <div className="stats">
                        <StatCard label="Current Price" value={`$${(data.price || 0).toFixed(2)}`} />
                        <StatCard label="Active Positions" value={data.active_positions} />
                        <StatCard label="Total Trades" value={data.total_trades} />
                        <StatCard label="Win Rate" value={`${(data.win_rate || 0).toFixed(1)}%`} />
                        <StatCard label="Total P&L" value={`$${(data.total_pnl || 0).toFixed(2)}`} type={data.total_pnl >= 0 ? 'profit' : 'loss'} />
                        <StatCard label="Today P&L" value={`$${(data.today_pnl || 0).toFixed(2)}`} type={data.today_pnl >= 0 ? 'profit' : 'loss'} />
                    </div>
                    
                    {/* Positions and Recent Trades */}
                    <div className="grid-2">
                        <div className="card">
                            <h2>📊 Active Positions</h2>
                            {data.positions.length === 0 ? (
                                <div className="empty">No active positions</div>
                            ) : (
                                data.positions.map((pos, idx) => (
                                    <div key={idx} className="card" style={{ marginBottom: '10px' }}>
                                        <strong>{pos.action} {pos.symbol}</strong> @ ${pos.entry_price.toFixed(2)}<br/>
                                        SL: ${pos.stop_loss.toFixed(2)} | TP: ${pos.take_profit.toFixed(2)}<br/>
                                        Qty: {pos.quantity.toFixed(4)} | Confidence: {(pos.confidence*100).toFixed(0)}%
                                    </div>
                                ))
                            )}
                        </div>
                        
                        <div className="card">
                            <h2>📋 Recent Trades</h2>
                            <table>
                                <thead>
                                    <tr>
                                        <th>Time</th>
                                        <th>Type</th>
                                        <th>Entry</th>
                                        <th>Exit</th>
                                        <th>P&L</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {data.recent_trades.length === 0 ? (
                                        <tr><td colSpan="5" className="empty">No trades yet</td></tr>
                                    ) : (
                                        data.recent_trades.slice(-5).map((t, idx) => (
                                            <tr key={idx}>
                                                <td>{new Date(t.exit_time).toLocaleTimeString()}</td>
                                                <td>{t.action}</td>
                                                <td>${t.entry_price.toFixed(2)}</td>
                                                <td>${t.exit_price.toFixed(2)}</td>
                                                <td className={t.pnl >= 0 ? 'profit' : 'loss'}>${t.pnl.toFixed(2)}</td>
                                            </tr>
                                        ))
                                    )}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            );
        }
        
        // Chart Tab Component
        function ChartTab({ data }) {
            const chartRef = useRef(null);
            
            useEffect(() => {
                if (chartRef.current && !chartRef.current.innerHTML) {
                    new TradingView.widget({
                        autosize: true,
                        symbol: "BINANCE:BTCUSDT",
                        interval: "1",
                        timezone: "Etc/UTC",
                        theme: "dark",
                        style: "1",
                        locale: "en",
                        toolbar_bg: "#1a1f3a",
                        enable_publishing: false,
                        allow_symbol_change: true,
                        container_id: "tradingview_chart"
                    });
                }
            }, []);
            
            return (
                <div className="card">
                    <h2>📈 Live Chart with Trade History</h2>
                    <div id="tradingview_chart" ref={chartRef} style={{ height: '600px' }}></div>
                    
                    <div style={{ marginTop: '20px', padding: '15px', background: 'rgba(0, 212, 255, 0.05)', borderRadius: '5px', borderLeft: '4px solid #00d4ff' }}>
                        <h3>📍 Trade History</h3>
                        {data.trade_history.length === 0 ? (
                            <div className="empty">No trade markers</div>
                        ) : (
                            data.trade_history.slice(-10).map((t, idx) => (
                                <div key={idx} style={{ borderLeft: `4px solid ${t.exit_price ? (t.exit_price > t.entry_price ? '#00ff88' : '#ff4466') : '#8b92b0'}`, padding: '10px', marginBottom: '8px', background: 'rgba(255,255,255,0.05)', borderRadius: '5px' }}>
                                    <strong>{t.entry_price > 0 ? '🟢 BUY' : '🔴 SELL'}</strong> @ ${t.entry_price.toFixed(2)}
                                    {t.exit_price && ` → EXIT @ $${t.exit_price.toFixed(2)} P&L: $${(t.exit_price - t.entry_price).toFixed(2)}`}
                                </div>
                            ))
                        )}
                    </div>
                </div>
            );
        }
        
        // Analytics Tab Component
        function AnalyticsTab({ data }) {
            const analytics = data.analytics;
            const pieChartRef = useRef(null);
            const barChartRef = useRef(null);
            const lineChartRef = useRef(null);
            const winRateChartRef = useRef(null);
            
            const chartInstances = useRef({});
            
            useEffect(() => {
                if (!analytics.win_loss_data) return;
                
                // Win/Loss Pie Chart
                if (pieChartRef.current) {
                    if (chartInstances.current.pie) chartInstances.current.pie.destroy();
                    chartInstances.current.pie = new Chart(pieChartRef.current, {
                        type: 'doughnut',
                        data: {
                            labels: ['🟢 Wins', '🔴 Losses', '⚪ Breaks'],
                            datasets: [{
                                data: [analytics.win_loss_data.wins, analytics.win_loss_data.losses, analytics.win_loss_data.breaks],
                                backgroundColor: ['#00ff88', '#ff4466', '#8b92b0'],
                                borderColor: ['#1a1f3a', '#1a1f3a', '#1a1f3a'],
                                borderWidth: 2
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: true,
                            plugins: {
                                legend: { labels: { color: '#8b92b0', font: { size: 12 }, padding: 15 } }
                            }
                        }
                    });
                }
                
                // Top Symbols Bar Chart
                if (barChartRef.current && analytics.top_symbols && analytics.top_symbols.length > 0) {
                    if (chartInstances.current.bar) chartInstances.current.bar.destroy();
                    const labels = analytics.top_symbols.map(s => s.symbol);
                    const pnlData = analytics.top_symbols.map(s => s.total_pnl);
                    const colors = pnlData.map(p => p >= 0 ? '#00ff88' : '#ff4466');
                    
                    chartInstances.current.bar = new Chart(barChartRef.current, {
                        type: 'bar',
                        data: {
                            labels: labels,
                            datasets: [{
                                label: 'Total P&L',
                                data: pnlData,
                                backgroundColor: colors,
                                borderColor: colors,
                                borderWidth: 1
                            }]
                        },
                        options: {
                            indexAxis: 'y',
                            responsive: true,
                            plugins: { legend: { labels: { color: '#8b92b0' } } },
                            scales: {
                                x: { ticks: { color: '#8b92b0' }, grid: { color: '#2a3155' } },
                                y: { ticks: { color: '#8b92b0' }, grid: { color: '#2a3155' } }
                            }
                        }
                    });
                }
                
                // Daily P&L Line Chart
                if (lineChartRef.current && analytics.pnl_by_date && analytics.pnl_by_date.length > 0) {
                    if (chartInstances.current.line) chartInstances.current.line.destroy();
                    const labels = analytics.pnl_by_date.map(s => new Date(s.trade_date).toLocaleDateString());
                    const pnlData = analytics.pnl_by_date.map(s => s.daily_pnl);
                    
                    chartInstances.current.line = new Chart(lineChartRef.current, {
                        type: 'line',
                        data: {
                            labels: labels,
                            datasets: [{
                                label: 'Daily P&L',
                                data: pnlData,
                                borderColor: '#00d4ff',
                                backgroundColor: 'rgba(0, 212, 255, 0.1)',
                                fill: true,
                                tension: 0.4,
                                pointRadius: 4
                            }]
                        },
                        options: {
                            responsive: true,
                            plugins: { legend: { labels: { color: '#8b92b0' } } },
                            scales: {
                                x: { ticks: { color: '#8b92b0' }, grid: { color: '#2a3155' } },
                                y: { ticks: { color: '#8b92b0' }, grid: { color: '#2a3155' } }
                            }
                        }
                    });
                }
                
                // Win Rate Trend Chart
                if (winRateChartRef.current && analytics.daily_stats && analytics.daily_stats.length > 0) {
                    if (chartInstances.current.winRate) chartInstances.current.winRate.destroy();
                    const labels = analytics.daily_stats.map(s => new Date(s.trade_date).toLocaleDateString());
                    const wrData = analytics.daily_stats.map(s => s.win_rate);
                    
                    chartInstances.current.winRate = new Chart(winRateChartRef.current, {
                        type: 'line',
                        data: {
                            labels: labels,
                            datasets: [{
                                label: 'Win Rate %',
                                data: wrData,
                                borderColor: '#00ff88',
                                backgroundColor: 'rgba(0, 255, 136, 0.1)',
                                fill: true,
                                tension: 0.4,
                                pointRadius: 4
                            }]
                        },
                        options: {
                            responsive: true,
                            plugins: { legend: { labels: { color: '#8b92b0' } } },
                            scales: {
                                y: { beginAtZero: true, max: 100, ticks: { color: '#8b92b0' }, grid: { color: '#2a3155' } },
                                x: { ticks: { color: '#8b92b0' }, grid: { color: '#2a3155' } }
                            }
                        }
                    });
                }
                
                return () => {
                    Object.values(chartInstances.current).forEach(chart => {
                        if (chart) chart.destroy();
                    });
                };
            }, [analytics]);
            
            return (
                <div>
                    <div className="stats">
                        <StatCard label="Total Trades" value={analytics.total_trades || 0} />
                        <StatCard label="Win Rate" value={`${(analytics.win_rate || 0).toFixed(1)}%`} />
                        <StatCard label="Total P&L" value={`$${(analytics.total_pnl || 0).toFixed(2)}`} type={analytics.total_pnl >= 0 ? 'profit' : 'loss'} />
                    </div>
                    
                    <div className="grid-2">
                        <div className="card">
                            <h3>🥧 Win/Loss Breakdown</h3>
                            <canvas ref={pieChartRef} height="200"></canvas>
                        </div>
                        
                        <div className="card">
                            <h3>📊 Top Performing Symbols</h3>
                            <canvas ref={barChartRef} height="200"></canvas>
                        </div>
                    </div>
                    
                    <div className="card">
                        <h3>📈 Daily P&L Trend (Last 30 Days)</h3>
                        <canvas ref={lineChartRef} height="100"></canvas>
                    </div>
                    
                    <div className="card">
                        <h3>📊 Win Rate Trend (Last 30 Days)</h3>
                        <canvas ref={winRateChartRef} height="100"></canvas>
                    </div>
                </div>
            );
        }
        
        // Journal Tab Component
        function JournalTab({ data }) {
            return (
                <div className="card">
                    <h2>📔 Trade Journal</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Date</th>
                                <th>Symbol</th>
                                <th>Type</th>
                                <th>Entry</th>
                                <th>Exit</th>
                                <th>P&L</th>
                            </tr>
                        </thead>
                        <tbody>
                            {data.recent_trades.length === 0 ? (
                                <tr><td colSpan="6" className="empty">No trades in journal</td></tr>
                            ) : (
                                data.recent_trades.map((t, idx) => (
                                    <tr key={idx}>
                                        <td>{new Date(t.exit_time).toLocaleDateString()}</td>
                                        <td>{t.symbol || 'N/A'}</td>
                                        <td>{t.action}</td>
                                        <td>${t.entry_price.toFixed(2)}</td>
                                        <td>${t.exit_price.toFixed(2)}</td>
                                        <td className={t.pnl >= 0 ? 'profit' : 'loss'}>${t.pnl.toFixed(2)}</td>
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </table>
                </div>
            );
        }
        
        // Performance Tab Component
        function PerformanceTab({ data }) {
            const analytics = data.analytics;
            return (
                <div>
                    <div className="stats">
                        <StatCard label="Total Trades" value={analytics.total_trades || 0} />
                        <StatCard label="Winning Trades" value={analytics.winning_trades || 0} />
                        <StatCard label="Win Rate" value={`${(analytics.win_rate || 0).toFixed(1)}%`} />
                        <StatCard label="Total P&L" value={`$${(analytics.total_pnl || 0).toFixed(2)}`} type={analytics.total_pnl >= 0 ? 'profit' : 'loss'} />
                    </div>
                    
                    <div className="card">
                        <h2>📊 Performance Breakdown</h2>
                        <div className="stats">
                            <StatCard label="30-Day Trades" value={analytics.trades_30_days || 0} />
                            <StatCard label="30-Day Win Rate" value={`${(analytics.win_rate_30 || 0).toFixed(1)}%`} />
                            <StatCard label="30-Day P&L" value={`$${(analytics.pnl_30_days || 0).toFixed(2)}`} type={analytics.pnl_30_days >= 0 ? 'profit' : 'loss'} />
                        </div>
                    </div>
                    
                    <div className="card">
                        <h2>📈 Key Metrics</h2>
                        <div style={{ padding: '15px', background: '#0a0e27', borderRadius: '5px', borderLeft: '4px solid #00d4ff' }}>
                            <p><strong>Avg Profit per Win:</strong> ${(data.avg_profit || 0).toFixed(2)}</p>
                            <p><strong>Avg Loss per Loss:</strong> ${Math.abs(data.avg_loss || 0).toFixed(2)}</p>
                            <p><strong>Profit Factor:</strong> {analytics.profit_factor ? (analytics.profit_factor).toFixed(2) : 'N/A'}</p>
                        </div>
                    </div>
                </div>
            );
        }
        
        // Stat Card Component
        function StatCard({ label, value, type = '' }) {
            return (
                <div className="stat-card">
                    <div className="stat-label">{label}</div>
                    <div className={`stat-value ${type}`}>{value}</div>
                </div>
            );
        }
        
        // Render App
        ReactDOM.createRoot(document.getElementById('root')).render(<App />);
    </script>
</body>
</html>
"""
