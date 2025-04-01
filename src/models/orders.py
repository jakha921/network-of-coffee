from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship


class OrderBase(SQLModel):
    """
    Order base schema
    
    Table orders {
        id int [pk, increment]
        user_id int
        total_price decimal(10,2)
        status varchar(50)
        created_at datetime [default: `now()`]
    }
    
    Ref: products.category_id > categories.id
    Ref: orders.user_id > users.id
    Ref: carts.user_id > users.id
    Ref: cart_items.cart_id > carts.id
    Ref: cart_items.product_id > products.id
    """
    name: str = Field(..., description="Product name")
    description: str = Field(..., description="Product description")
    price: int = Field(..., description="Product price")
    category_id: int = Field(..., description="Category ID")


class Order(OrderBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)

    # Relationships
    category: "Category" = Relationship(back_populates="products")
