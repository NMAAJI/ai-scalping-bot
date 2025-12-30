#!/bin/bash
# Build script for React frontend
# This script builds the React app and copies it to the web/static folder

cd "$(dirname "$0")"

echo "🏗️ Building React frontend..."

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Build the app
echo "📦 Building production bundle..."
npm run build

# Check if build succeeded
if [ ! -d "build" ]; then
    echo "❌ Build failed!"
    exit 1
fi

# Create static folders if they don't exist
mkdir -p ../web/static/js
mkdir -p ../web/static/css
mkdir -p ../web/static/media

# Copy built files
echo "📂 Copying build files..."
cp build/index.html ../web/templates/
cp -r build/static/* ../web/static/

echo "✅ Build complete!"
echo "Frontend files copied to web/static/"
