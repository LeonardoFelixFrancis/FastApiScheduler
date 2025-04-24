from pydantic import BaseModel
from typing import Optional

class UserFilters(BaseModel):
    id: int | None = None
    username: str | None = None
    email: str | None = None
    name: Optional[str] = None
    company_id: int | None = None
