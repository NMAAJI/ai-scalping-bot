import os
import sys

# Add the project root to the python path so we can import main
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

# Vercel will look for the 'app' variable here to handle requests