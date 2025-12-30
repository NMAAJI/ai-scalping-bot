#!/usr/bin/env python3
"""
AI Trading Bot Startup Script
Production-ready application entry point
"""

import sys
import logging
from pathlib import Path

# Ensure project root is in path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# Setup logging early
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/trading_bot.log')
    ]
)

logger = logging.getLogger(__name__)

def verify_requirements():
    """Verify all requirements are installed"""
    required_packages = [
        'binance',
        'dotenv',
        'google.generativeai',
        'flask',
        'requests',
        'pandas',
        'numpy',
        'ta'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        logger.error(f"Missing packages: {', '.join(missing)}")
        logger.error("Install with: pip install -r requirements.txt")
        return False
    
    return True

def verify_environment():
    """Verify .env file and API keys"""
    env_file = PROJECT_ROOT / '.env'
    
    if not env_file.exists():
        logger.error(".env file not found!")
        logger.error("Copy .env.example to .env and fill in your API keys")
        return False
    
    # Load and check
    from dotenv import load_dotenv
    load_dotenv()
    
    import os
    required_keys = ['BINANCE_API_KEY', 'BINANCE_API_SECRET', 'GEMINI_API_KEY']
    missing_keys = [key for key in required_keys if not os.getenv(key)]
    
    if missing_keys:
        logger.error(f"Missing API keys: {', '.join(missing_keys)}")
        return False
    
    logger.info("✅ All API keys configured")
    return True

def verify_directories():
    """Verify required directories exist"""
    dirs = ['logs', 'data']
    
    for dir_name in dirs:
        dir_path = PROJECT_ROOT / dir_name
        dir_path.mkdir(exist_ok=True)
    
    logger.info("✅ Directories verified")
    return True

def main():
    """Start the application"""
    logger.info("")
    logger.info("=" * 70)
    logger.info("🤖 AI TRADING BOT - PRODUCTION EDITION")
    logger.info("=" * 70)
    logger.info("")
    
    # Verify environment
    logger.info("Verifying requirements...")
    if not verify_requirements():
        logger.error("❌ Requirements check failed")
        sys.exit(1)
    
    logger.info("Verifying configuration...")
    if not verify_environment():
        logger.error("❌ Configuration check failed")
        sys.exit(1)
    
    logger.info("Verifying directories...")
    if not verify_directories():
        logger.error("❌ Directory check failed")
        sys.exit(1)
    
    logger.info("")
    
    # Import and run main app
    from main import app, initialize_services, auto_engine
    
    if not initialize_services():
        logger.error("❌ Failed to initialize services")
        sys.exit(1)
    
    logger.info("")
    logger.info("✅ All checks passed!")
    logger.info("📈 Starting web server...")
    logger.info(f"🌐 Open your browser: http://localhost:5000")
    logger.info("")
    
    try:
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,
            use_reloader=False
        )
    except KeyboardInterrupt:
        logger.info("\n🛑 Shutting down...")
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
