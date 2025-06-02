from pydantic import BaseModel

class StudentInputSchema(BaseModel):
    name: str

class StudentOutputSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class StudentSchemaFilter(BaseModel):
    id: int | None = None
    name: str | None = None