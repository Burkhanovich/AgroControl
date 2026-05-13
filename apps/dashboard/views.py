from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from config.settings import settings
from config.security import get_current_user
from apps.authentication.models import User

router = APIRouter()
templates = Jinja2Templates(directory=str(settings.TEMPLATES_DIR))


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    """Dashboard sahifasi - JavaScript orqali authentication"""
    return templates.TemplateResponse(
        "dashboard/index.html",
        {"request": request}
    )


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Bosh sahifa - login ga yo'naltirish"""
    return templates.TemplateResponse("auth/login.html", {"request": request})
