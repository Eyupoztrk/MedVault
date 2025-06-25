from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    date_of_birth: Optional[date]
    gender: Optional[str]

class UserResponse(BaseModel):
    id: str
    full_name: str
    email: EmailStr
    date_of_birth: Optional[date]
    gender: Optional[str]

    class Config:
        orm_mode = True