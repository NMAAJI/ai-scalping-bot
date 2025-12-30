/**
 * API Client
 * Handles all communication with Flask backend
 */

const API_BASE_URL = 'http://localhost:5000/api';

export const apiClient = {
    // Get current status
    async getStatus() {
        try {
            const response = await fetch(`${API_BASE_URL}/status`);
            return await response.json();
        } catch (error) {
            console.error('Error fetching status:', error);
            throw error;
        }
    },

    // Get analytics data
    async getAnalytics() {
        try {
            const response = await fetch(`${API_BASE_URL}/analytics`);
            return await response.json();
        } catch (error) {
            console.error('Error fetching analytics:', error);
            throw error;
        }
    },

    // Get trade history
    async getTradeHistory() {
        try {
            const response = await fetch(`${API_BASE_URL}/trade-history`);
            return await response.json();
        } catch (error) {
            console.error('Error fetching trade history:', error);
            throw error;
        }
    },

    // Toggle auto-trading
    async toggleAutoTrading() {
        try {
            const response = await fetch(`${API_BASE_URL}/toggle-auto`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            return await response.json();
        } catch (error) {
            console.error('Error toggling auto-trading:', error);
            throw error;
        }
    },

    // Get market data
    async getMarketData() {
        try {
            const response = await fetch(`${API_BASE_URL}/market-data`);
            return await response.json();
        } catch (error) {
            console.error('Error fetching market data:', error);
            throw error;
        }
    },

    // Get performance metrics
    async getPerformanceMetrics() {
        try {
            const response = await fetch(`${API_BASE_URL}/performance`);
            return await response.json();
        } catch (error) {
            console.error('Error fetching performance metrics:', error);
            throw error;
        }
    }
};

export default apiClient;
