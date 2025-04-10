from pydantic import BaseModel
from typing import Optional

class UserFilters(BaseModel):
    id: Optional[int] = None
    username: Optional[str] = None
    email: Optional[str] = None
    name: Optional[str] = None
