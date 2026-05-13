from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from config.database import get_db
from config.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    validate_password_strength,
    get_current_user
)
from config.settings import settings
from apps.authentication.models import User
from apps.authentication.schemas import UserCreate, UserLogin, TokenResponse, UserResponse
from apps.farms.models import Farm
from apps.zones.models import Zone, Sensor

router = APIRouter()
templates = Jinja2Templates(directory=str(settings.TEMPLATES_DIR))


# HTML Pages
@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login sahifasi"""
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Register sahifasi"""
    return templates.TemplateResponse("auth/register.html", {"request": request})


# API Endpoints
@router.post("/api/auth/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Yangi foydalanuvchi ro'yxatdan o'tkazish"""

    # Email mavjudligini tekshirish
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bu email allaqachon ro'yxatdan o'tgan",
        )

    # Fermer xo'jaligini yaratish
    farm = None
    if user_data.farm_name and user_data.farm_location:
        farm = Farm(
            name=user_data.farm_name,
            location=user_data.farm_location,
            total_area_hectares=0.0,
        )
        db.add(farm)
        db.flush()

    # Foydalanuvchini yaratish
    user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        phone=user_data.phone,
        password_hash=get_password_hash(user_data.password),
        language=user_data.language,
        role="farmer",
        farm_id=farm.id if farm else None,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Farm owner_id ni yangilash
    if farm:
        farm.owner_id = user.id
        db.commit()

    # Token yaratish
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserResponse.model_validate(user),
    )


@router.post("/api/auth/login", response_model=TokenResponse)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Foydalanuvchi tizimga kirishi"""

    # Foydalanuvchini topish
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email yoki parol noto'g'ri",
        )

    # Parolni tekshirish
    if not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email yoki parol noto'g'ri",
        )

    # Faol ekanligini tekshirish
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Foydalanuvchi faol emas",
        )

    # Token yaratish
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserResponse.model_validate(user),
    )
