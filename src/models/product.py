from sqlalchemy import Column, String, Text, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship
from src.models.base import BaseModel

class Product(BaseModel):
    __tablename__ = "products"

    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    price = Column(Float)
    image_url = Column(String, nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    
    category = relationship("Category", back_populates="products")
    cart_items = relationship("CartItem", back_populates="product") 