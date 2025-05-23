from flask import Flask, jsonify, render_template
from flask_cors import CORS
from airoco import get_sensor_data
import requests

app = Flask(__name__, static_folder='static')
CORS(app)

NODE_RED_URL = "http://localhost:1880/receive-data"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/data")
def get_data():
    try:
        data = get_sensor_data()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/send-to-nodered")
def send_to_nodered():
    try:
        data = get_sensor_data()
        response = requests.post(NODE_RED_URL, json=data)
        if response.status_code == 200:
            return jsonify({"status": "sent", "response": response.text})
        else:
            return jsonify({"error": "Failed to send", "status_code": response.status_code}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)
