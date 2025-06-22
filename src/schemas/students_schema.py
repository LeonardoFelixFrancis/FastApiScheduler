from pydantic import BaseModel
from typing import TypedDict, NamedTuple

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

class StudentAttendanceOutputSchema(BaseModel):
    id: int
    name: str
    attended: bool

class StudentSchemaFilter(BaseModel):
    id: int | None = None
    name: str | None = None
    company_id: int | None = None

class StudentsDBResponse(NamedTuple):
    id: int
    name: str
    lesson_id: int
    company_id: int