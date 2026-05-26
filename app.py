from flask import Flask, jsonify
from datetime import datetime, timezone

app = Flask(__name__)

MISSION = "SPACE CONNECT"
VERSION = "1.0"

@app.route('/')
def index():
    return jsonify({
        "mission": MISSION,
        "version": VERSION,
        "status": "ONLINE",
        "timestamp": datetime.now(timezone.utc).isoformat()
    })

@app.route('/health')
def health():
    return jsonify({
        "mission": MISSION,
        "version": VERSION,
        "status": "ONLINE",
        "timestamp": datetime.now(timezone.utc).isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
