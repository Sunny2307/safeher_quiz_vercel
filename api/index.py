"""
Vercel serverless function wrapper for Flask app
This file acts as the entry point for Vercel's Python runtime
"""
import sys
import os

try:
    # Add parent directory to Python path so we can import from model
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)

    # Change working directory to parent for file access
    # This ensures CSV files can be found relative to model directory
    os.chdir(parent_dir)
    
    # Import the Flask app from model directory
    from model.app import app
    
    # Export the app - Vercel's Python runtime will handle WSGI conversion automatically
    # The @vercel/python builder converts Flask apps to serverless functions
    
except Exception as e:
    # If import fails, create a minimal error handler
    from flask import Flask, jsonify
    app = Flask(__name__)
    
    @app.route('/health')
    @app.route('/<path:path>')
    def error_handler(path=''):
        return jsonify({
            "error": "Failed to initialize Flask app",
            "message": str(e),
            "path": path
        }), 500

