from pydantic import BaseModel, EmailStr

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
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True