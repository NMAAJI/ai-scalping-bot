/**
 * Dashboard Component
 * Main dashboard container with tabs and state management
 */

import React, { useState, useEffect } from 'react';
import apiClient from '../utils/api';
import { REFRESH_INTERVAL, DEFAULT_STATE } from '../utils/constants';
import Overview from './Overview';
import Chart from './Chart';
import Analytics from './Analytics';
import Journal from './Journal';
import Performance from './Performance';
import '../styles/dashboard.css';

export default function Dashboard() {
    const [activeTab, setActiveTab] = useState('overview');
    const [data, setData] = useState(DEFAULT_STATE);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [lastUpdate, setLastUpdate] = useState(null);

    // Fetch all data
    const fetchData = async () => {
        try {
            setError(null);
            const [status, analytics, history, market, performance] = await Promise.all([
                apiClient.getStatus(),
                apiClient.getAnalytics(),
                apiClient.getTradeHistory(),
                apiClient.getMarketData(),
                apiClient.getPerformanceMetrics()
            ]);

            setData(prev => ({
                ...prev,
                ...status,
                analytics,
                trade_history: history.trades || [],
                market_data: market,
                performance_metrics: performance
            }));

            setLastUpdate(new Date().toLocaleTimeString());
            setLoading(false);
        } catch (err) {
            console.error('Error fetching data:', err);
            setError('Failed to fetch data. Retrying...');
        }
    };

    // Setup polling
    useEffect(() => {
        fetchData(); // Initial fetch
        
        const interval = setInterval(fetchData, REFRESH_INTERVAL);
        return () => clearInterval(interval);
    }, []);

    // Toggle auto-trading
    const handleToggleAutoTrading = async () => {
        try {
            const result = await apiClient.toggleAutoTrading();
            setData(prev => ({ ...prev, bot_running: result.running }));
        } catch (err) {
            console.error('Error toggling auto-trading:', err);
            setError('Failed to toggle auto-trading');
        }
    };

    // Render active tab
    const renderTab = () => {
        const props = {
            data,
            loading,
            error,
            lastUpdate,
            onToggleAutoTrading: handleToggleAutoTrading
        };

        switch (activeTab) {
            case 'overview':
                return <Overview {...props} />;
            case 'chart':
                return <Chart {...props} />;
            case 'analytics':
                return <Analytics {...props} />;
            case 'journal':
                return <Journal {...props} />;
            case 'performance':
                return <Performance {...props} />;
            default:
                return <Overview {...props} />;
        }
    };

    return (
        <div className="dashboard-container">
            {/* Header */}
            <div className="dashboard-header">
                <div className="dashboard-title">
                    <span>🤖</span>
                    <span>AI Trading Bot Dashboard</span>
                </div>
            </div>

            {/* Tabs */}
            <div className="tab-container">
                <button
                    className={`tab-button ${activeTab === 'overview' ? 'active' : ''}`}
                    onClick={() => setActiveTab('overview')}
                >
                    📊 Overview
                </button>
                <button
                    className={`tab-button ${activeTab === 'chart' ? 'active' : ''}`}
                    onClick={() => setActiveTab('chart')}
                >
                    📈 Chart
                </button>
                <button
                    className={`tab-button ${activeTab === 'analytics' ? 'active' : ''}`}
                    onClick={() => setActiveTab('analytics')}
                >
                    📉 Analytics
                </button>
                <button
                    className={`tab-button ${activeTab === 'journal' ? 'active' : ''}`}
                    onClick={() => setActiveTab('journal')}
                >
                    📓 Journal
                </button>
                <button
                    className={`tab-button ${activeTab === 'performance' ? 'active' : ''}`}
                    onClick={() => setActiveTab('performance')}
                >
                    🏆 Performance
                </button>
            </div>

            {/* Content */}
            {error && (
                <div style={{ background: 'rgba(255, 68, 102, 0.1)', padding: '15px', borderRadius: '5px', marginBottom: '20px', color: '#ff4466' }}>
                    {error}
                </div>
            )}

            {renderTab()}
        </div>
    );
}
