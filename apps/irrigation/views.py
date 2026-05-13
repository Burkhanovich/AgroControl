"""
Irrigation views - API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List

from config.database import get_db
from config.security import get_current_user
from config.settings import settings
from apps.authentication.models import User
from apps.irrigation.service import irrigation_service
from apps.irrigation.schemas import SensorWithReadings, DashboardStats

router = APIRouter()
templates = Jinja2Templates(directory=str(settings.TEMPLATES_DIR))


@router.get("/api/sensors", response_model=List[SensorWithReadings])
async def get_sensors(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Barcha datchiklar va oxirgi o'lchovlar"""
    if not current_user.farm_id:
        raise HTTPException(status_code=400, detail="Fermer xo'jaligi topilmadi")
    
    return irrigation_service.get_sensors_with_latest_readings(db, current_user.farm_id)


@router.get("/api/dashboard/stats", response_model=DashboardStats)
async def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Dashboard statistikasi"""
    if not current_user.farm_id:
        raise HTTPException(status_code=400, detail="Fermer xo'jaligi topilmadi")
    
    return irrigation_service.get_dashboard_stats(db, current_user.farm_id)


@router.post("/api/sensors/demo")
async def generate_demo_data(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Demo ma'lumotlar yaratish"""
    if not current_user.farm_id:
        raise HTTPException(status_code=400, detail="Fermer xo'jaligi topilmadi")
    
    irrigation_service.generate_demo_readings(db, current_user.farm_id)
    return {"message": "Demo ma'lumotlar yaratildi"}


@router.get("/irrigation", response_class=HTMLResponse)
async def irrigation_page(request: Request):
    """Sug'orish sahifasi"""
    return templates.TemplateResponse(
        "irrigation/index.html",
        {"request": request}
    )
# Force reload
