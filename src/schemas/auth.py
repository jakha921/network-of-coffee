from pydantic import Field
from pydantic import EmailStr
from pydantic import BaseModel


class SUserAuth(BaseModel):
    email: EmailStr = Field(..., example="user@exmple.com")
    password: str = Field(..., example="12345678")


class SUserPassword(BaseModel):
    email: EmailStr = Field(..., example="user@exmple.com")
    password: str = Field(..., example="12345678")
    new_password: str = Field(..., example="123321")
