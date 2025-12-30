/**
 * App.jsx
 * Main React Application Entry Point
 */

import React from 'react';
import Dashboard from './components/Dashboard';
import './styles/globals.css';
import './styles/dashboard.css';
import './styles/tables.css';

export default function App() {
    return (
        <div className="container">
            <Dashboard />
        </div>
    );
}
