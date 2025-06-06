from pydantic import BaseModel

class StudentInputSchema(BaseModel):
    name: str

class StudentUpdateInput(BaseModel):
    id: int
    name: str

class StudentOutputSchema(BaseModel):
    id: int
    name: str
    company_id: int

    class Config:
        from_attributes = True

class StudentSchemaFilter(BaseModel):
    id: int | None = None
    name: str | None = None
    company_id: int | None = None