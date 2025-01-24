from flask import Flask, request, jsonify
from flask_cors import CORS
from weatherClass import WeatherService
from weeklySummaryClass import WeeklySummaryService
import os

class FlaskApp:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)
        self.weather_service = WeatherService()
        self.weekly_service = WeeklySummaryService()
        self.register_routes()

    def register_routes(self):
        self.app.route("/")(self.home)
        self.app.route("/forecast", methods=["GET"])(self.forecast)
        self.app.route("/weekly_summary", methods=["GET"])(self.weekly_summary)

    def home(self):
        return jsonify({
            "status": "running",
            "endpoints": [
                "/forecast?lat=52.2&lon=21",
                "/weekly_summary?lat=52.2&lon=21"
            ]
        })

    def forecast(self):
        lat = request.args.get("lat")
        lon = request.args.get("lon")
        if not lat or not lon:
            return jsonify({"error": "Missing parameters. Use: /forecast?lat=52.2&lon=21"}), 400
        
        data = self.weather_service.get_weather(lat, lon)
        return jsonify(data)

    def weekly_summary(self):
        lat = request.args.get("lat")
        lon = request.args.get("lon")
        if not lat or not lon:
            return jsonify({"error": "Missing parameters. Use: /weekly_summary?lat=52.2&lon=21"}), 400
            
        data = self.weekly_service.get_weather_summary(lat, lon)
        return jsonify(data)

    def run(self):
        self.app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

flask_app = FlaskApp()
app = flask_app.app

if __name__ == "__main__":
    flask_app.run()