from pydantic import BaseModel

class ResetPasswordSchema(BaseModel):
    password: str
    confirm_password: str