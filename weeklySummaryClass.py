import requests

class WeeklySummaryService:
    def get_weather_summary(self, lat, lon):
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": "pressure_msl",
            "daily": "temperature_2m_max,temperature_2m_min,daylight_duration,precipitation_hours,wind_speed_10m_max",
            "timezone": "auto",
            "models": "ukmo_seamless"
        }
        try:
            resp = requests.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()
            hourly = data.get("hourly", {})
            daily = data.get("daily", {})

            press = hourly.get("pressure_msl", [])
            avg_press = sum(press) / len(press) if press else None

            day_dur = daily.get("daylight_duration", [])
            avg_sun = sum(day_dur) / len(day_dur) if day_dur else None

            tmax = daily.get("temperature_2m_max", [])
            tmin = daily.get("temperature_2m_min", [])
            max_temp = max(tmax) if tmax else None
            min_temp = min(tmin) if tmin else None

            phours = daily.get("precipitation_hours", [])
            p_days = len([x for x in phours if x > 0])
            w_summary = "z opadami" if p_days > 3 else "bez opadów"

            wind_speeds = daily.get("wind_speed_10m_max", [])
            wind_avg = sum(wind_speeds) / len(wind_speeds) if wind_speeds else None

            return {
                "averagePressure": avg_press,
                "averageSunshineDuration": avg_sun,
                "maxTemperature": max_temp,
                "minTemperature": min_temp,
                "precipitationDays": p_days,
                "weatherSummary": w_summary,
                "windAverage": wind_avg
            }
        except Exception as e:
            print("Error fetching API:", e)
            return {}