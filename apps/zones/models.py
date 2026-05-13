import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from config.database import Base
from config.database_types import UUID


class Zone(Base):
    """Dala zonalari modeli"""
    __tablename__ = "zones"

    id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    farm_id = Column(UUID(), ForeignKey("farms.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    area_hectares = Column(Float, nullable=False)
    crop_type = Column(String(100), nullable=True)
    polygon_coordinates = Column(JSON, nullable=True)
    target_moisture_min = Column(Integer, default=50)
    target_moisture_max = Column(Integer, default=70)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    farm = relationship("Farm", back_populates="zones")
    sensors = relationship("Sensor", back_populates="zone", cascade="all, delete-orphan", lazy="dynamic")
    irrigation_schedules = relationship("IrrigationSchedule", back_populates="zone", lazy="dynamic")
    irrigation_logs = relationship("IrrigationLog", back_populates="zone", lazy="dynamic")

    def __repr__(self):
        return f"<Zone {self.name}>"


class Sensor(Base):
    """Datchik modeli"""
    __tablename__ = "sensors"

    id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    zone_id = Column(UUID(), ForeignKey("zones.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)  # soil_moisture, temperature, ph, etc.
    is_active = Column(String(20), default="active")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    zone = relationship("Zone", back_populates="sensors")
    readings = relationship("SensorReading", back_populates="sensor")

    def __repr__(self):
        return f"<Sensor {self.name}>"
