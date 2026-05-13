from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, UUID4


# Base schemas
class UserBase(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=255)
    email: EmailStr
    phone: str = Field(..., min_length=9, max_length=20)
    language: str = Field(default="uz", pattern="^(uz|ru)$")


class UserCreate(UserBase):
    password: str = Field(..., min_length=1, max_length=100)
    farm_name: Optional[str] = None
    farm_location: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(UserBase):
    id: UUID4
    role: str
    farm_id: Optional[UUID4]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse
