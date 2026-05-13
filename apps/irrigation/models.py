"""
Irrigation models - Sug'orish va datchik modellari
"""
from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from datetime import datetime
from config.database import Base
from config.database_types import UUID
import uuid


class IrrigationSchedule(Base):
    """Sug'orish jadvali"""
    __tablename__ = "irrigation_schedules"

    id = Column(UUID, primary_key=True, default=lambda: str(uuid.uuid4()))
    zone_id = Column(UUID, ForeignKey("zones.id"), nullable=False)
    name = Column(String(100), nullable=False)
    start_time = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    repeat_days = Column(String(50))
    water_amount = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    zone = relationship("Zone", back_populates="irrigation_schedules")
    logs = relationship("IrrigationLog", back_populates="schedule")


class IrrigationLog(Base):
    """Sug'orish tarixi"""
    __tablename__ = "irrigation_logs"

    id = Column(UUID, primary_key=True, default=lambda: str(uuid.uuid4()))
    schedule_id = Column(UUID, ForeignKey("irrigation_schedules.id"), nullable=False)
    zone_id = Column(UUID, ForeignKey("zones.id"), nullable=False)
    started_at = Column(DateTime, nullable=False)
    completed_at = Column(DateTime)
    water_used = Column(Float)
    status = Column(String(20))
    notes = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)

    schedule = relationship("IrrigationSchedule", back_populates="logs")
    zone = relationship("Zone", back_populates="irrigation_logs")


class SensorReading(Base):
    """Datchik o'lchovlari"""
    __tablename__ = "sensor_readings"

    id = Column(UUID, primary_key=True, default=lambda: str(uuid.uuid4()))
    sensor_id = Column(UUID, ForeignKey("sensors.id"), nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String(20))
    timestamp = Column(DateTime, default=datetime.utcnow)
    is_alert = Column(Boolean, default=False)
    alert_message = Column(String(200))

    sensor = relationship("Sensor", back_populates="readings")
