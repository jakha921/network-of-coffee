from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship


class CategoryBase(SQLModel):
    """
    Category base schema
    
    Table categories {
        id int [pk, increment]
        name varchar(100)
        description text
    }
    
    Ref: products.category_id > categories.id
    Ref: orders.user_id > users.id
    Ref: carts.user_id > users.id
    Ref: cart_items.cart_id > carts.id
    Ref: cart_items.product_id > products.id
    """
    name: str = Field(..., description="Category name")
    description: str = Field(..., description="Category description")


class Category(CategoryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)

    # Relationships
    products: List["Product"] = Relationship(back_populates="category")
