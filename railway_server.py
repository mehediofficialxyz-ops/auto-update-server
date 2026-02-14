from flask import Flask, jsonify, send_file, request
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
CURRENT_VERSION = "1.0.0"
APP_FILE = "test_app.exe"

@app.route('/version')
def get_version():
    """Return current version information"""
    # Railway automatically provides the URL
    download_url = f"{request.host_url}/download"
    return jsonify({
        "version": CURRENT_VERSION,
        "download_url": download_url,
        "release_notes": "Initial release"
    })

@app.route('/download')
def download_app():
    """Download the latest version"""
    if os.path.exists(APP_FILE):
        return send_file(APP_FILE, as_attachment=True, download_name=APP_FILE)
    else:
        return jsonify({"error": "File not found"}), 404

@app.route('/health')
def health_check():
    """Health check for Railway"""
    return jsonify({"status": "healthy", "version": CURRENT_VERSION})

@app.route('/')
def home():
    """Home page with status"""
    return f"""
    <h1>Auto Update Server - Railway</h1>
    <p>Current Version: {CURRENT_VERSION}</p>
    <p>Available endpoints:</p>
    <ul>
        <li><a href="/version">/version</a> - Get version info</li>
        <li><a href="/download">/download</a> - Download latest version</li>
        <li><a href="/health">/health</a> - Health check</li>
    </ul>
    """

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
