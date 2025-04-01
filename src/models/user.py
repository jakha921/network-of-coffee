from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, String, Boolean, Enum, Integer, DateTime
from sqlalchemy.orm import relationship
import enum
from src.models.base import BaseModel

class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"

class User(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    role = Column(Enum(UserRole), default=UserRole.USER)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    cart = relationship("Cart", back_populates="user", uselist=False)
    orders = relationship("Order", back_populates="user")

    def __repr__(self):
        return f"<User {self.id} {self.email}>"
