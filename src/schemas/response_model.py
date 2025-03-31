from pydantic import BaseModel
from typing import Any, Optional

class ResponseModel(BaseModel):
    status: str
    message: str
    data: Optional[Any]