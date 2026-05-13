"""
Weather service - OpenWeatherMap API integration
"""
import httpx
from typing import Optional, Dict, Any
from datetime import datetime
from config.settings import settings
from config.logging_config import logger


class WeatherService:
    """Ob-havo xizmati"""

    BASE_URL = "https://api.openweathermap.org/data/2.5"

    def __init__(self):
        self.api_key = settings.OPENWEATHER_API_KEY

    async def get_current_weather(self, lat: float, lon: float) -> Optional[Dict[str, Any]]:
        """Joriy ob-havo ma'lumotlarini olish"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.BASE_URL}/weather",
                    params={
                        "lat": lat,
                        "lon": lon,
                        "appid": self.api_key,
                        "units": "metric",
                        "lang": "uz"
                    },
                    timeout=10.0
                )

                if response.status_code == 200:
                    data = response.json()
                    return {
                        "temp": round(data["main"]["temp"]),
                        "feels_like": round(data["main"]["feels_like"]),
                        "humidity": data["main"]["humidity"],
                        "pressure": data["main"]["pressure"],
                        "wind_speed": round(data["wind"]["speed"], 1),
                        "description": data["weather"][0]["description"],
                        "icon": data["weather"][0]["icon"],
                        "city": data.get("name", ""),
                    }
                else:
                    logger.error(f"Weather API error: {response.status_code}")
                    return None

        except Exception as e:
            logger.error(f"Weather service error: {str(e)}")
            return None

    async def get_forecast(self, lat: float, lon: float) -> Optional[list]:
        """7 kunlik ob-havo prognozi"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.BASE_URL}/forecast",
                    params={
                        "lat": lat,
                        "lon": lon,
                        "appid": self.api_key,
                        "units": "metric",
                        "lang": "uz"
                    },
                    timeout=10.0
                )

                if response.status_code == 200:
                    data = response.json()

                    # Kunlik prognozni guruhlash (har kuni 12:00 vaqtini olish)
                    daily_forecast = []
                    seen_dates = set()

                    for item in data["list"]:
                        dt = datetime.fromtimestamp(item["dt"])
                        date_str = dt.strftime("%Y-%m-%d")

                        # Har bir kun uchun faqat bitta ma'lumot (12:00 atrofida)
                        if date_str not in seen_dates and dt.hour >= 11 and dt.hour <= 13:
                            seen_dates.add(date_str)
                            daily_forecast.append({
                                "date": date_str,
                                "day_name": self._get_day_name(dt.weekday()),
                                "temp_max": round(item["main"]["temp_max"]),
                                "temp_min": round(item["main"]["temp_min"]),
                                "humidity": item["main"]["humidity"],
                                "description": item["weather"][0]["description"],
                                "icon": item["weather"][0]["icon"],
                                "wind_speed": round(item["wind"]["speed"], 1),
                                "pop": round(item.get("pop", 0) * 100)  # Precipitation probability
                            })

                            if len(daily_forecast) >= 7:
                                break

                    return daily_forecast
                else:
                    logger.error(f"Forecast API error: {response.status_code}")
                    return None

        except Exception as e:
            logger.error(f"Forecast service error: {str(e)}")
            return None

    def _get_day_name(self, weekday: int) -> str:
        """Hafta kuni nomini olish"""
        days = {
            0: "Dushanba",
            1: "Seshanba",
            2: "Chorshanba",
            3: "Payshanba",
            4: "Juma",
            5: "Shanba",
            6: "Yakshanba"
        }
        return days.get(weekday, "")


# Global instance
weather_service = WeatherService()
