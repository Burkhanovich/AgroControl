import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base
from config.database_types import UUID


class Farm(Base):
    """Fermer xo'jaliklari modeli"""
    __tablename__ = "farms"

    id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    location = Column(String(500), nullable=False)
    total_area_hectares = Column(Float, nullable=False)
    owner_id = Column(UUID(), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    owner = relationship("User", foreign_keys=[owner_id], back_populates="owned_farm")
    users = relationship("User", foreign_keys="User.farm_id", back_populates="farm")
    zones = relationship("Zone", back_populates="farm", cascade="all, delete-orphan", lazy="dynamic")

    def __repr__(self):
        return f"<Farm {self.name}>"
