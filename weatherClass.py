import requests

class WeatherService:
    def get_weather(self, lat, lon):
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "daily": "weather_code,temperature_2m_max,temperature_2m_min,sunrise,sunset,daylight_duration,sunshine_duration,precipitation_hours",
            "models": "ukmo_seamless",
            "timezone": "auto"
        }
        try:
            resp = requests.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()
            daily = data.get("daily", {})

            time_data = daily.get("time", [])
            weather_code = daily.get("weather_code", [])
            temp_max = daily.get("temperature_2m_max", [])
            temp_min = daily.get("temperature_2m_min", [])
            daylight = daily.get("daylight_duration", [])

            installation_power = 2.5
            panel_efficiency = 0.2
            estimated_energy = []
            for dur in daylight:
                hours_of_daylight = dur / 3600
                estimated_energy.append(installation_power * hours_of_daylight * panel_efficiency)

            result = []
            for i in range(len(time_data)):
                result.append({
                    "date": time_data[i],
                    "weatherCode": weather_code[i] if i < len(weather_code) else None,
                    "temperature2mMax": temp_max[i] if i < len(temp_max) else None,
                    "temperature2mMin":  temp_min[i] if i < len(temp_min) else None,
                    "estimatedEnergy":   estimated_energy[i] if i < len(estimated_energy) else None
                })

            return result
        except Exception as e:
            print("Error fetching API:", e)
            return []