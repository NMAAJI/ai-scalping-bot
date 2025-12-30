/**
 * Helper Functions
 * Utility functions for formatting, calculations, etc.
 */

export const formatCurrency = (value) => {
    if (value === null || value === undefined) return '$0.00';
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    }).format(value);
};

export const formatPercent = (value) => {
    if (value === null || value === undefined) return '0.00%';
    return `${value.toFixed(2)}%`;
};

export const formatNumber = (value, decimals = 2) => {
    if (value === null || value === undefined) return '0.00';
    return parseFloat(value).toFixed(decimals);
};

export const getStatusColor = (status) => {
    const colors = {
        'RUNNING': '#00ff88',
        'STOPPED': '#ff4466',
        'PAUSED': '#ffaa00',
        'BUY': '#00ff88',
        'SELL': '#ff4466',
        'HOLD': '#ffaa00'
    };
    return colors[status] || '#8b92b0';
};

export const getStatusBg = (status) => {
    const backgrounds = {
        'RUNNING': 'rgba(0, 255, 136, 0.1)',
        'STOPPED': 'rgba(255, 68, 102, 0.1)',
        'PAUSED': 'rgba(255, 170, 0, 0.1)',
    };
    return backgrounds[status] || 'transparent';
};

export const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    try {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    } catch (error) {
        return dateString;
    }
};

export const calculateROI = (initialAmount, finalAmount) => {
    if (initialAmount === 0) return 0;
    return ((finalAmount - initialAmount) / initialAmount) * 100;
};

export const calculateWinRate = (wins, total) => {
    if (total === 0) return 0;
    return (wins / total) * 100;
};

export const getProfitColor = (value) => {
    if (value > 0) return '#00ff88';
    if (value < 0) return '#ff4466';
    return '#8b92b0';
};

export const formatTimestamp = (timestamp) => {
    if (!timestamp) return 'N/A';
    const date = new Date(timestamp * 1000);
    return date.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
};

export const debounce = (func, wait) => {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
};
