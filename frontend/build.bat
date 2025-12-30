@echo off
REM Build script for React frontend (Windows)
REM This script builds the React app and copies it to the web/static folder

echo.
echo ======================================
echo Building React Frontend...
echo ======================================
echo.

REM Check if node_modules exists
if not exist "node_modules" (
    echo 📦 Installing dependencies...
    call npm install
    if errorlevel 1 (
        echo ❌ npm install failed!
        exit /b 1
    )
)

REM Build the app
echo 📦 Building production bundle...
call npm run build
if errorlevel 1 (
    echo ❌ Build failed!
    exit /b 1
)

REM Check if build succeeded
if not exist "build" (
    echo ❌ Build folder not found!
    exit /b 1
)

REM Create static folders if they don't exist
if not exist "..\web\static\js" mkdir ..\web\static\js
if not exist "..\web\static\css" mkdir ..\web\static\css
if not exist "..\web\static\media" mkdir ..\web\static\media
if not exist "..\web\templates" mkdir ..\web\templates

REM Copy built files
echo 📂 Copying build files...
xcopy /E /Y "build\index.html" "..\web\templates\"
xcopy /E /Y "build\static\*" "..\web\static\"

echo.
echo ✅ Build complete!
echo Frontend files copied to web/static/
echo.
pause
