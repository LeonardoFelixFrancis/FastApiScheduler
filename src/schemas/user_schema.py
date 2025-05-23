from pydantic import BaseModel, EmailStr
from typing import Optional

class AdmCreate(BaseModel):
    username: str
    name: str
    email: EmailStr
    password: str
    company_name: str

class UserCreate(BaseModel):
    username: str
    name: str
    email: EmailStr
    password: str | None = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True