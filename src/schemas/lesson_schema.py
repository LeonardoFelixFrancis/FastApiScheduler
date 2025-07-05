from pydantic import BaseModel, validator
from typing import Optional
from src.schemas.students_schema import StudentOutputSchema
import datetime

class LessonSchema(BaseModel):
    id: int | None = None
    lesson_name: str
    lesson_subject: str
    students: list[int] | None = None

class LessonOutput(BaseModel):
    id: int | None = None
    lesson_name: str
    lesson_subject: str
    students: list[StudentOutputSchema] | None = None

    class Config:
        from_attributes = True

class LessonFilter(BaseModel):
    id: int | None = None
    lesson_name: str | None = None
    lesson_subject: str | None = None
    students: list[int] | None = None
    company_id: int | None = None
    active: bool | None = None

class LessonScheduleSchema(BaseModel):
    id: int | None = None
    lesson_id: int
    date: datetime.date
    time: datetime.time 
    teacher_id: int
    teacher_name: str | None = None
    lesson_name: str | None = None

class LessonScheduleSchemaResponse(BaseModel):
    id: int
    lesson_id: int
    date: datetime.date
    time: datetime.time
    teacher_id: int
    teacher_name: str
    teacher_active: bool
    lesson_name: str
    company_id: int
    lesson_active: bool

    class Config:
        from_attributes = True
        json_encoders = {
            datetime.time: lambda t: t.strftime('%H:%M')
        }

class LessonScheduleFilter(BaseModel):
    id: int | None = None
    lesson_id: int | None = None 
    date: Optional[datetime.date] = None
    time: Optional[datetime.time] = None
    company_id: int | None = None
    teacher_id: int | None = None
    date_start: Optional[datetime.date] = None
    date_end: Optional[datetime.date] = None
    active: bool | None = None

class StudentAttendanceInputSchema(BaseModel):
    students_who_attended: list[int]
    schedule_id: int