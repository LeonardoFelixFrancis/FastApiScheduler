from pydantic import BaseModel
from typing import Optional
import datetime

class LessonSchema(BaseModel):
    id: int | None = None
    lesson_name: str
    lesson_subject: str
    students: list[str] | None = None

class LessonFilter(BaseModel):
    id: int | None = None
    lesson_name: str | None = None
    lesson_subject: str | None = None
    students: list[str] | None = None
    company_id: int | None = None

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
    lesson_name: str
    company_id: int

class LessonScheduleFilter(BaseModel):
    id: int | None = None
    lesson_id: int | None = None 
    date: Optional[datetime.date] = None
    time: Optional[datetime.time] = None
    company_id: int | None = None
    teacher_id: int | None = None
    date_start: Optional[datetime.date] = None
    date_end: Optional[datetime.date] = None