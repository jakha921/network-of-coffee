from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from src.models.base import BaseModel

class Cart(BaseModel):
    __tablename__ = "carts"

    user_id = Column(Integer, ForeignKey("users.id"))
    total_amount = Column(Float, default=0.0)

    user = relationship("User", back_populates="cart")
    items = relationship("CartItem", back_populates="cart")

class CartItem(BaseModel):
    __tablename__ = "cart_items"

    cart_id = Column(Integer, ForeignKey("carts.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=1)
    price = Column(Float)

    cart = relationship("Cart", back_populates="items")
    product = relationship("Product", back_populates="cart_items") 