from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship


class ProductBase(SQLModel):
    """
    Product base schema
    
    Table products {
        id int [pk, increment]
        name varchar(100)
        description text
        price decimal(10,2)
        category_id int
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


class Product(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)

    # Relationships
    category: "Category" = Relationship(back_populates="products")
    