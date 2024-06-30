from flask import Flask, send_from_directory, jsonify
import os

app = Flask(__name__)
PACKAGE_DIR = 'packages'

@app.route('/<path:filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(PACKAGE_DIR, filename)

@app.route('/packages', methods=['GET'])
def list_packages():
    try:
        packages = os.listdir(PACKAGE_DIR)
        return jsonify(packages)
    except Exception as e:
        return str(e), 500

def start_server(host='0.0.0.0', port=5000):
    os.makedirs(PACKAGE_DIR, exist_ok=True)
    app.run(host=host, port=port)

