"""
Irrigation service - Sug'orish va datchik xizmatlari
"""
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from datetime import datetime, timedelta
from typing import List, Optional
import random

from apps.irrigation.models import IrrigationSchedule, IrrigationLog, SensorReading
from apps.zones.models import Zone, Sensor
from apps.irrigation.schemas import SensorWithReadings, DashboardStats


class IrrigationService:
    """Sug'orish xizmatlari"""

    @staticmethod
    def get_sensors_with_latest_readings(db: Session, farm_id: str) -> List[SensorWithReadings]:
        """Barcha datchiklar va oxirgi o'lchovlar"""
        latest_reading = db.query(
            SensorReading.sensor_id,
            func.max(SensorReading.timestamp).label('max_timestamp')
        ).group_by(SensorReading.sensor_id).subquery()

        sensors = db.query(
            Sensor,
            Zone.name.label('zone_name'),
            SensorReading.value,
            SensorReading.unit,
            SensorReading.timestamp,
            SensorReading.is_alert
        ).join(Zone).outerjoin(
            latest_reading,
            Sensor.id == latest_reading.c.sensor_id
        ).outerjoin(
            SensorReading,
            (SensorReading.sensor_id == Sensor.id) &
            (SensorReading.timestamp == latest_reading.c.max_timestamp)
        ).filter(Zone.farm_id == farm_id).all()

        result = []
        for sensor, zone_name, value, unit, timestamp, is_alert in sensors:
            result.append(SensorWithReadings(
                id=sensor.id,
                name=sensor.name,
                type=sensor.type,
                zone_name=zone_name,
                latest_value=value,
                latest_unit=unit,
                latest_timestamp=timestamp,
                is_alert=is_alert or False,
                status="active" if sensor.is_active else "inactive"
            ))

        return result

    @staticmethod
    def get_dashboard_stats(db: Session, farm_id: str) -> DashboardStats:
        """Dashboard statistikasi"""
        total_zones = db.query(Zone).filter(Zone.farm_id == farm_id).count()
        
        active_zones = db.query(Zone).join(IrrigationSchedule).filter(
            Zone.farm_id == farm_id,
            IrrigationSchedule.is_active == True
        ).distinct().count()

        total_sensors = db.query(Sensor).join(Zone).filter(
            Zone.farm_id == farm_id
        ).count()

        alert_sensors = db.query(Sensor).join(Zone).join(SensorReading).filter(
            Zone.farm_id == farm_id,
            SensorReading.is_alert == True
        ).distinct().count()

        today = datetime.utcnow().date()
        today_water = db.query(func.sum(IrrigationLog.water_used)).join(Zone).filter(
            Zone.farm_id == farm_id,
            func.date(IrrigationLog.started_at) == today
        ).scalar() or 0.0

        active_schedules = db.query(IrrigationSchedule).join(Zone).filter(
            Zone.farm_id == farm_id,
            IrrigationSchedule.is_active == True
        ).count()

        return DashboardStats(
            total_zones=total_zones,
            active_zones=active_zones,
            total_sensors=total_sensors,
            alert_sensors=alert_sensors,
            today_water_usage=round(today_water, 2),
            active_schedules=active_schedules
        )

    @staticmethod
    def generate_demo_readings(db: Session, farm_id: str):
        """Demo ma'lumotlar generatsiya qilish"""
        sensors = db.query(Sensor).join(Zone).filter(Zone.farm_id == farm_id).all()

        for sensor in sensors:
            if sensor.type == "soil_moisture":
                value = random.uniform(30, 80)
                unit = "%"
                is_alert = value < 40 or value > 75
            elif sensor.type == "temperature":
                value = random.uniform(15, 35)
                unit = "°C"
                is_alert = value > 30
            elif sensor.type == "ph":
                value = random.uniform(5.5, 8.0)
                unit = "pH"
                is_alert = value < 6.0 or value > 7.5
            else:
                value = random.uniform(0, 100)
                unit = "unit"
                is_alert = False

            reading = SensorReading(
                sensor_id=sensor.id,
                value=round(value, 2),
                unit=unit,
                is_alert=is_alert,
                alert_message=f"Ogohlantirish: {sensor.name}" if is_alert else None,
                timestamp=datetime.utcnow()
            )
            db.add(reading)

        db.commit()


irrigation_service = IrrigationService()
