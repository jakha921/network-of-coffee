from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.database import get_db
from src.models.cart import Cart, CartItem
from src.models.product import Product
from src.dependencies import get_current_active_user
from src.models.user import User

router = APIRouter()

@router.post("/cart")
async def add_to_cart(
    product_id: int,
    quantity: int = 1,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    
    cart_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == product_id
    ).first()
    
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=product_id,
            quantity=quantity,
            price=product.price
        )
        db.add(cart_item)
    
    # Обновляем общую сумму корзины
    cart.total_amount = sum(item.price * item.quantity for item in cart.items)
    
    db.commit()
    db.refresh(cart_item)
    return cart_item

@router.get("/cart")
async def get_cart():
    return {"message": "Cart contents"}

@router.delete("/cart/{item_id}")
async def remove_from_cart(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    cart_item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.cart_id == cart.id
    ).first()
    
    if not cart_item:
        raise HTTPException(status_code=404, detail="Item not found in cart")
    
    db.delete(cart_item)
    
    # Обновляем общую сумму корзины
    cart.total_amount = sum(item.price * item.quantity for item in cart.items)
    
    db.commit()
    return {"message": "Item removed from cart"}

@router.delete("/cart")
async def clear_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
    cart.total_amount = 0.0
    db.commit()
    return {"message": "Cart cleared"} 