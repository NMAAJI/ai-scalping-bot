import os
import sys

# Add the project root directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

# Import the Flask app from main.py
from main import app, initialize_services

# Initialize services (connect to Binance, AI, etc.)
# This runs on every cold start of the serverless function
initialize_services()

# Vercel looks for the 'app' variable in this file
# We expose the app imported from main.py