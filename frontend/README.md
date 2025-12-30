# React Frontend - AI Trading Bot Dashboard

Professional React-based frontend for the AI Trading Bot with modular components, comprehensive styling, and full API integration.

## 📁 Project Structure

```
frontend/
├── public/
│   └── index.html          # Main HTML template
├── src/
│   ├── components/         # React components
│   │   ├── Dashboard.jsx   # Main container with tabs
│   │   ├── Overview.jsx    # Statistics & status
│   │   ├── Chart.jsx       # Price charts & indicators
│   │   ├── Analytics.jsx   # Detailed analytics
│   │   ├── Journal.jsx     # Trade journal
│   │   └── Performance.jsx # Performance metrics
│   ├── utils/              # Utility functions
│   │   ├── api.js          # API client
│   │   ├── helpers.js      # Helper functions
│   │   └── constants.js    # Constants & config
│   ├── styles/             # CSS files
│   │   ├── globals.css     # Global styles
│   │   ├── dashboard.css   # Dashboard styles
│   │   └── tables.css      # Tables & charts
│   ├── App.jsx             # Main App component
│   └── index.jsx           # React entry point
├── package.json            # Dependencies
├── build.bat              # Build script (Windows)
└── build.sh               # Build script (Unix/Mac)
```

## 🚀 Getting Started

### Prerequisites
- Node.js 14+ and npm
- Python 3.8+ (for backend Flask server)

### Installation

1. **Install Frontend Dependencies**
```bash
cd frontend
npm install
```

2. **Build the React App**
```bash
# Windows
build.bat

# Unix/Mac
bash build.sh
```

The build process will:
- Bundle the React app
- Copy files to `web/static/`
- Update Flask to serve the React app

### Development Mode

```bash
cd frontend
npm start
```

This starts a development server with hot reload on `http://localhost:3000`

## 🎯 Components & Features

### Dashboard Component
- Central hub with tab navigation
- Real-time data polling (3-second intervals)
- API error handling
- Loading states

### Overview Tab
- Bot status indicator with live pulse
- Key statistics (8 metrics)
- Recent trades table
- Start/Stop buttons

### Chart Tab
- Price chart visualization
- Technical indicators (RSI, MACD, Volume)
- Trend analysis
- Signal indicators

### Analytics Tab
- Performance metrics grid
- Win/Loss distribution chart
- Profit/Loss trend chart
- Daily statistics table

### Journal Tab
- Complete trade history
- Entry/exit prices
- P&L calculations
- Trade duration tracking

### Performance Tab
- Sharpe ratio, Drawdown, Profit Factor
- Monthly performance breakdown
- Performance goals display
- ROI calculations

## 🎨 Styling System

### CSS Architecture
- **globals.css**: Base styles, animations, utilities
- **dashboard.css**: Component-specific styles
- **tables.css**: Tables and charts styling

### Color Scheme
```css
--color-primary: #00d4ff (Cyan)
--color-success: #00ff88 (Green)
--color-danger: #ff4466 (Red)
--color-warning: #ffaa00 (Orange)
--color-dark: #0a0e27 (Dark background)
--color-text: #ffffff (White text)
--color-text-muted: #8b92b0 (Muted gray)
```

### Responsive Design
- Mobile-first approach
- Breakpoints: 768px, 1024px
- Flexible grid layouts
- Touch-friendly buttons

## 📡 API Integration

### API Client (`utils/api.js`)
- `getStatus()` - Bot status & statistics
- `getAnalytics()` - Analytics data
- `getTradeHistory()` - Trade history
- `toggleAutoTrading()` - Start/Stop bot
- `getMarketData()` - Market data
- `getPerformanceMetrics()` - Performance metrics

### Endpoints
All endpoints are relative to `/api/`:
- `GET /status` - Current bot status
- `GET /analytics` - Analytics data
- `GET /trade-history` - Trade history
- `POST /toggle-auto` - Toggle auto-trading
- `GET /market-data` - Market data
- `GET /performance` - Performance metrics

## 🛠️ Development

### Add New Component
1. Create `src/components/ComponentName.jsx`
2. Import in `Dashboard.jsx`
3. Add tab button and route

### Add New Styles
1. Create CSS file in `src/styles/`
2. Import in component
3. Use CSS variables for colors

### Update API Integration
1. Add function in `src/utils/api.js`
2. Call in component with `apiClient.functionName()`
3. Handle loading/error states

## 📊 Data Flow

```
React Component
     ↓
API Client (utils/api.js)
     ↓
Flask Backend (/api/*)
     ↓
Python Services (Auto Engine, Executor, etc.)
     ↓
Binance API & Gemini AI
     ↓
SQLite Database
```

## 🔧 Configuration

### API Base URL
Default: `http://localhost:5000/api`
Change in `src/utils/api.js` if needed

### Refresh Interval
Default: 3 seconds
Change in `src/utils/constants.js`:
```javascript
export const REFRESH_INTERVAL = 3000;
```

### Colors & Theme
Change CSS variables in `src/styles/globals.css`:
```css
:root {
    --color-primary: #00d4ff;
    --color-success: #00ff88;
    /* ... */
}
```

## 📦 Build Output

After building, files are organized as:
```
web/
├── templates/
│   └── index.html      # Main React HTML
└── static/
    ├── js/
    │   └── main.js     # React JS bundle
    ├── css/
    │   └── main.css    # CSS bundle
    └── media/          # Images & assets
```

Flask serves these files automatically.

## 🐛 Troubleshooting

### Build fails
- Clear `node_modules/` and reinstall: `npm install`
- Check Node.js version: `node --version`

### API not connecting
- Ensure Flask is running: `python main.py`
- Check API Base URL in `src/utils/api.js`
- Check browser console for errors

### Styling issues
- Clear browser cache
- Check CSS variable imports
- Verify file paths in imports

### Hot reload not working
- Kill development server and restart
- Check for port conflicts
- Install dependencies again

## 📝 Notes

- React app is embedded as fallback (REACT_DASHBOARD in Python)
- Production build recommended for deployment
- API expects JSON responses
- Polling interval can be adjusted for performance

## 🎓 Learning Resources

- [React 18 Docs](https://react.dev)
- [Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)
- [CSS Grid](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Grid_Layout)
- [Chart.js](https://www.chartjs.org/)

## 📄 License

Same as main AI Trading Bot project
