"""
Weather views - API endpoints
"""
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from apps.weather.service import weather_service
from apps.weather.schemas import WeatherResponse, CurrentWeather, DailyForecast
from config.security import get_current_user
from config.settings import settings
from apps.authentication.models import User

router = APIRouter()
templates = Jinja2Templates(directory=str(settings.TEMPLATES_DIR))


@router.get("/api/weather", response_model=WeatherResponse)
async def get_weather(
    lat: float = 41.2995,  # Toshkent koordinatalari (default)
    lon: float = 69.2401,
    current_user: User = Depends(get_current_user)
):
    """
    Ob-havo ma'lumotlarini olish

    Parameters:
    - lat: Kenglik (latitude)
    - lon: Uzunlik (longitude)
    """

    # Joriy ob-havo
    current = await weather_service.get_current_weather(lat, lon)

    # 7 kunlik prognoz
    forecast = await weather_service.get_forecast(lat, lon)

    if current is None or forecast is None:
        raise HTTPException(
            status_code=503,
            detail="Ob-havo xizmatiga ulanishda xatolik"
        )

    return WeatherResponse(
        current=CurrentWeather(**current),
        forecast=[DailyForecast(**day) for day in forecast],
        location=current.get("city", "Toshkent")
    )


@router.get("/weather", response_class=HTMLResponse)
async def weather_page(request: Request):
    """Ob-havo sahifasi"""
    return templates.TemplateResponse(
        "weather/index.html",
        {"request": request}
    )
