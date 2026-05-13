import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base
from config.database_types import UUID


class User(Base):
    """Foydalanuvchilar modeli"""
    __tablename__ = "users"

    id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default="farmer")  # admin, farmer, technician
    farm_id = Column(UUID(), ForeignKey("farms.id", ondelete="CASCADE"), nullable=True)
    language = Column(String(2), default="uz")  # uz, ru
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    farm = relationship("Farm", foreign_keys=[farm_id], back_populates="users")
    owned_farm = relationship("Farm", foreign_keys="Farm.owner_id", back_populates="owner", uselist=False)

    def __repr__(self):
        return f"<User {self.email}>"
