from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    name: str
    email: EmailStr
    password: str
    is_teacher: bool
    is_adm: bool

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True