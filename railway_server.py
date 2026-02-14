from flask import Flask, jsonify, send_file, request
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuration
CURRENT_VERSION = "1.0.1"
APP_FILE = "test_app_safe.exe"

@app.route('/')
def home():
    """Home page with status"""
    return jsonify({
        "message": "Auto Update Server - Railway",
        "version": CURRENT_VERSION,
        "status": "running",
        "endpoints": {
            "version": "/version",
            "download": "/download", 
            "health": "/health"
        }
    })

@app.route('/version')
def get_version():
    """Return current version information"""
    # Get the current request URL
    base_url = request.host_url
    download_url = f"{base_url}download"
    
    return jsonify({
        "version": CURRENT_VERSION,
        "download_url": download_url,
        "release_notes": "Initial release",
        "server_url": base_url
    })

@app.route('/download')
def download_app():
    """Download the latest version"""
    if os.path.exists(APP_FILE):
        return send_file(APP_FILE, as_attachment=True, download_name=APP_FILE)
    else:
        return jsonify({
            "error": "File not found",
            "message": f"Looking for: {APP_FILE}",
            "available_files": os.listdir('.') if os.path.exists('.') else []
        }), 404

@app.route('/health')
def health_check():
    """Health check for Railway"""
    return jsonify({
        "status": "healthy", 
        "version": CURRENT_VERSION,
        "files": os.listdir('.') if os.path.exists('.') else []
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    print(f"Starting server on port {port}")
    app.run(host='0.0.0.0', port=port)
