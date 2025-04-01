from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr




class UserBase(BaseModel):
    uuid: Optional[str] = None
    email: Optional[EmailStr] = None
    old_email: Optional[str] = None
    password: Optional[str] = None
    name: Optional[str] = None
    stripe_customer_id: Optional[str] = None
    kids_age: Optional[int] = None
    hero: Optional[str] = None
    interests: Optional[List[str]] = None


class SUserCreate(UserBase):
    pass


class SUserUpdate(UserBase):
    pass


class SUserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    interests: Optional[List[str]] = []
    selected_interests: Optional[List[str]] = []
    child_level: Optional[str] = None

    class Config:
        from_attributes = True


example_user = SUserRead(
    id=1,
    email="john@doe.com",
    old_email="doe@john.com",
    name="John Doe",
    created_at=datetime.now(),
    updated_at=datetime.now(),
    interests=[],
    selected_interests=[]

)
