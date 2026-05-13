import os
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "AgroControl"
    VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Security
    SECRET_KEY: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # Database
    DATABASE_URL: str

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # InfluxDB
    INFLUXDB_URL: str = "http://localhost:8086"
    INFLUXDB_TOKEN: str
    INFLUXDB_ORG: str = "agrocontrol"
    INFLUXDB_BUCKET: str = "sensors"

    # MQTT
    MQTT_BROKER: str = "localhost"
    MQTT_PORT: int = 1883

    # OpenWeatherMap API
    OPENWEATHER_API_KEY: str = ""

    # Templates & Static
    TEMPLATES_DIR: Path = BASE_DIR / "templates"
    STATIC_DIR: Path = BASE_DIR / "static"

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:8000", "http://localhost"]

    @field_validator("SECRET_KEY", "JWT_SECRET_KEY")
    @classmethod
    def validate_secret_keys(cls, v: str, info) -> str:
        """Secret key validatsiyasi"""
        if len(v) < 32:
            raise ValueError(f"{info.field_name} kamida 32 ta belgidan iborat bo'lishi kerak")
        if v.startswith("your-") or v.startswith("jwt-secret"):
            raise ValueError(
                f"{info.field_name} default qiymatda qoldirilgan! "
                "Iltimos, .env faylida kuchli secret key o'rnating"
            )
        return v

    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Database URL validatsiyasi"""
        if not v:
            raise ValueError("DATABASE_URL bo'sh bo'lishi mumkin emas")
        return v

    class Config:
        env_file = ".env"
        case_sensitive = True


def validate_settings():
    """Settings validatsiyasi va startup check"""
    try:
        settings = Settings()
        print("[OK] Settings validatsiyasi muvaffaqiyatli")
        return settings
    except Exception as e:
        print(f"[ERROR] Settings validatsiyasi xato: {e}")
        print("\nIltimos, .env faylini tekshiring:")
        print("  - SECRET_KEY va JWT_SECRET_KEY kamida 32 ta belgi")
        print("  - Default qiymatlarni o'zgartiring")
        print("  - DATABASE_URL to'g'ri formatda")
        raise


settings = validate_settings()
