from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from weatherClass import WeatherService
from weeklySummaryClass import WeeklySummaryService

class FastAPIApp:
    def __init__(self):
        self.app = FastAPI()
        self.weather_service = WeatherService()
        self.weekly_service = WeeklySummaryService()
        self.setup_cors()
        self.setup_routes()

    def setup_cors(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def setup_routes(self):
        @self.app.get("/")
        async def home():
            return {
                "status": "running",
                "endpoints": [
                    "/forecast?lat=52.2&lon=21",
                    "/weekly_summary?lat=52.2&lon=21"
                ]
            }

        @self.app.get("/forecast")
        async def forecast(lat: float, lon: float):
            if not lat or not lon:
                raise HTTPException(status_code=400, detail="Missing parameters")
            return self.weather_service.get_weather(lat, lon)

        @self.app.get("/weekly_summary")
        async def weekly_summary(lat: float, lon: float):
            if not lat or not lon:
                raise HTTPException(status_code=400, detail="Missing parameters")
            return self.weekly_service.get_weather_summary(lat, lon)

app = FastAPIApp().app