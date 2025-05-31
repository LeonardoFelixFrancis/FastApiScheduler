from pydantic import BaseModel
from datetime import datetime

class PasswordResetSchema(BaseModel):
    id: int | None = None
    token: str
    minutes_to_live: int
    created_at: datetime | None = None
    user_id: int
    active: bool | None = None