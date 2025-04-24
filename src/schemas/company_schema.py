from pydantic import BaseModel

class CompanySchema(BaseModel):
    id: int | None
    name: str

class CompanyFilter(BaseModel):
    id: int | None
    name: str | None