from pydantic import BaseModel
from typing import Optional

class UserFilters(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    name: Optional[str] = None
