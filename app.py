from flask import Flask, request, jsonify
from weatherClass import WeatherService

app = Flask(__name__)
weather_service = WeatherService()

@app.route("/forecast", methods=["GET"])
def forecast():
    lat = request.args.get("lat", "52.2")
    lon = request.args.get("lon", "21")
    if not lat or not lon:
        return jsonify({"error": "Missing required parameters"}), 400

    data = weather_service.get_weather(lat, lon)
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)