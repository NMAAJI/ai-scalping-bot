from flask import Flask, jsonify, request
from flask_cors import CORS
import os

# Initialize Flask App
app = Flask(__name__)
CORS(app)

@app.route('/api/health')
def health():
    """Health check endpoint to verify deployment"""
    return jsonify({
        "status": "online",
        "message": "AI Scalping Bot API is running",
        "version": "1.0.0"
    })

# Add your bot routes here or import them
# from my_bot_logic import bp as bot_bp
# app.register_blueprint(bot_bp)

@app.route('/api/<path:path>')
def catch_all(path):
    return jsonify({"error": "Endpoint not found", "path": path}), 404

# Note: Vercel looks for the 'app' variable in this file.