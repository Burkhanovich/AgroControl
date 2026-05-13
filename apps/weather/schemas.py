"""
Weather models
"""
from pydantic import BaseModel
from typing import Optional


class CurrentWeather(BaseModel):
    """Joriy ob-havo"""
    temp: int
    feels_like: int
    humidity: int
    pressure: int
    wind_speed: float
    description: str
    icon: str
    city: str


class DailyForecast(BaseModel):
    """Kunlik prognoz"""
    date: str
    day_name: str
    temp_max: int
    temp_min: int
    humidity: int
    description: str
    icon: str
    wind_speed: float
    pop: int  # Precipitation probability (%)


class WeatherResponse(BaseModel):
    """Ob-havo javobi"""
    current: Optional[CurrentWeather]
    forecast: list[DailyForecast]
    location: str
