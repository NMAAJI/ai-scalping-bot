# React Frontend Setup Guide

## Quick Start

### Step 1: Install Dependencies
```bash
cd frontend
npm install
```

### Step 2: Build React App
```bash
# Windows
build.bat

# Linux/Mac
bash build.sh
```

### Step 3: Start Flask Backend
```bash
# From root directory
python main.py
```

### Step 4: Open Dashboard
```
http://localhost:5000
```

## What Was Created

### React Components
- ✅ Dashboard.jsx - Main container with tabs
- ✅ Overview.jsx - Statistics & status
- ✅ Chart.jsx - Price charts
- ✅ Analytics.jsx - Detailed analytics
- ✅ Journal.jsx - Trade history
- ✅ Performance.jsx - Performance metrics

### Styling (CSS)
- ✅ globals.css - Global styles & animations
- ✅ dashboard.css - Dashboard component styles
- ✅ tables.css - Tables & charts styling

### Utilities (JavaScript)
- ✅ api.js - API client for Flask backend
- ✅ helpers.js - Formatting & utility functions
- ✅ constants.js - Constants & configuration

### Files Generated
- ✅ src/App.jsx - Main React app
- ✅ src/index.jsx - React entry point
- ✅ public/index.html - HTML template
- ✅ package.json - Dependencies
- ✅ build.bat / build.sh - Build scripts

## Architecture

```
Frontend (React) ←→ Backend (Flask) ←→ Services (Python)
     ↓
  Components
  State Management
  API Calls
  Styling
     ↓
  Compiled to static files
     ↓
  Served by Flask
```

## File Organization

```
frontend/
├── src/
│   ├── components/       # React UI components
│   ├── utils/           # API & helpers
│   ├── styles/          # CSS files
│   ├── App.jsx
│   └── index.jsx
├── public/
│   └── index.html       # HTML template
├── package.json
├── build.bat            # Windows build
└── build.sh             # Unix/Mac build

web/
├── templates/           # HTML (after build)
└── static/              # JS, CSS, media (after build)
```

## Development Workflow

1. **Modify React code** in `frontend/src/`
2. **Rebuild** using `build.bat` or `build.sh`
3. **Refresh browser** to see changes
4. **Check console** for errors

## Important Notes

- Flask must be running for API calls to work
- React app polls API every 3 seconds
- Embedded React dashboard is fallback if build not available
- All styles are responsive (mobile-friendly)
- Color scheme is dark theme with cyan accents

## Next Steps

1. ✅ Components created
2. ✅ Styling completed
3. ✅ API integration ready
4. Run `build.bat` to create production files
5. Start Flask and open dashboard

## Troubleshooting

### npm install fails
```bash
rm -rf node_modules package-lock.json
npm install
```

### build.bat not working
- Ensure Node.js is installed
- Check you're in frontend folder
- Run as administrator

### API errors in console
- Verify Flask is running
- Check API base URL in api.js
- Ensure endpoints match Flask routes

## Support

See `/frontend/README.md` for detailed documentation
