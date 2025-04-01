from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from src.models.base import BaseModel

class Category(BaseModel):
    __tablename__ = "categories"

    name = Column(String, unique=True, index=True)
    description = Column(Text, nullable=True)
    slug = Column(String, unique=True, index=True)
    
    products = relationship("Product", back_populates="category") 