"""
Irrigation schemas - Pydantic models
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class SensorReadingBase(BaseModel):
    value: float
    unit: str
    is_alert: bool = False
    alert_message: Optional[str] = None


class SensorReadingCreate(SensorReadingBase):
    sensor_id: str


class SensorReadingResponse(SensorReadingBase):
    id: str
    sensor_id: str
    timestamp: datetime

    class Config:
        from_attributes = True


class SensorWithReadings(BaseModel):
    id: str
    name: str
    type: str
    zone_name: str
    latest_value: Optional[float] = None
    latest_unit: Optional[str] = None
    latest_timestamp: Optional[datetime] = None
    is_alert: bool = False
    status: str = "active"


class IrrigationScheduleBase(BaseModel):
    name: str
    start_time: datetime
    duration_minutes: int
    repeat_days: Optional[str] = None
    water_amount: Optional[float] = None
    is_active: bool = True


class IrrigationScheduleCreate(IrrigationScheduleBase):
    zone_id: str


class IrrigationScheduleUpdate(BaseModel):
    name: Optional[str] = None
    start_time: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    repeat_days: Optional[str] = None
    water_amount: Optional[float] = None
    is_active: Optional[bool] = None


class IrrigationScheduleResponse(IrrigationScheduleBase):
    id: str
    zone_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class IrrigationLogResponse(BaseModel):
    id: str
    schedule_id: str
    zone_id: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    water_used: Optional[float] = None
    status: str
    notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class DashboardStats(BaseModel):
    total_zones: int
    active_zones: int
    total_sensors: int
    alert_sensors: int
    today_water_usage: float
    active_schedules: int
