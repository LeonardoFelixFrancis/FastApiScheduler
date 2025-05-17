from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LessonSchema(BaseModel):
    id: int | None = None
    lesson_name: str
    lesson_subject: str
    students: list[str]
    teacher_id: int

class LessonFilter(BaseModel):
    id: int | None = None
    lesson_name: str | None = None
    lesson_subject: str | None = None
    students: list[str] | None = None
    teacher_id: int | None = None
    company_id: int | None = None

class LessonScheduleSchema(BaseModel):
    id: int | None = None
    lesson_id: int
    scheduled_at: datetime
    minutes_duration: int

class LessonScheduleUpdateSchema(BaseModel):
    id: int | None = None
    scheduled_at: datetime
    minutes_duration: int

class LessonScheduleFilter(BaseModel):
    id: int | None = None
    lesson_id: int | None = None 
    scheduled_at: Optional[datetime] = None
    scheduled_at_begin: Optional[datetime] = None
    scheduled_at_end: Optional[datetime] = None
    company_id: int | None = None
    minutes_duration: int | None = None
    teacher_id: int | None = None