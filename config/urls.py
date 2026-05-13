from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from config.settings import settings
from config.logging_config import logger

# FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="O'zbekiston fermerlariga mo'ljallangan dala sug'orish boshqaruv tizimi"
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global xatolik handler"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Ichki server xatoligi",
            "error": str(exc) if settings.DEBUG else "Internal server error"
        }
    )

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["Content-Type", "Authorization"],
)

# Static files
app.mount("/static", StaticFiles(directory=str(settings.STATIC_DIR)), name="static")

# Templates
templates = Jinja2Templates(directory=str(settings.TEMPLATES_DIR))

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Import routers
from apps.authentication.views import router as auth_router
from apps.dashboard.views import router as dashboard_router
from apps.weather.views import router as weather_router
from apps.irrigation.views import router as irrigation_router

# Import all models to register them with SQLAlchemy
from apps.authentication.models import User
from apps.farms.models import Farm
from apps.zones.models import Zone, Sensor
from apps.irrigation.models import IrrigationSchedule, IrrigationLog, SensorReading

# API v1 routers
app.include_router(auth_router, tags=["authentication"])
app.include_router(dashboard_router, tags=["dashboard"])
app.include_router(weather_router, tags=["weather"])
app.include_router(irrigation_router, tags=["irrigation"])
