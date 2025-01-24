from flask import Flask, request, jsonify
from flask_cors import CORS
from weatherClass import WeatherService
from weeklySummaryClass import WeeklySummaryService
import os

app = Flask(__name__)
CORS(app)
weather_service = WeatherService()
weekly_service = WeeklySummaryService()

@app.route("/")
def home():
    return jsonify({
        "status": "running",
        "endpoints": [
            "/forecast?lat=52.2&lon=21",
            "/weekly_summary?lat=52.2&lon=21"
        ]
    })

@app.route("/forecast", methods=["GET"])
def forecast():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    if not lat or not lon:
        return jsonify({"error": "Missing parameters. Use: /forecast?lat=52.2&lon=21"}), 400

    data = weather_service.get_weather(lat, lon)
    return jsonify(data)

@app.route("/weekly_summary", methods=["GET"])
def weekly_summary():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    if not lat or not lon:
        return jsonify({"error": "Missing parameters. Use: /weekly_summary?lat=52.2&lon=21"}), 400

    summary = weekly_service.get_weather_summary(lat, lon)
    return jsonify(summary)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))