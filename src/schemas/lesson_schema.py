from pydantic import BaseModel
from typing import Optional
import datetime

class LessonSchema(BaseModel):
    id: int
    lesson_name: str
    lesson_subject: str
    students: list[str]
    teacher_id: int

class LessonFilter(BaseModel):
    id: Optional[int] = None
    lesson_name: Optional[str] = None
    lesson_subject: Optional[str] = None
    students: Optional[list[str]] = None
    teacher_id: Optional[int] = None

class LessonScheduleSchema(BaseModel):
    id: int
    lesson_id: int
    date: datetime.date
    time: datetime.time 

class LessonScheduleFilter(BaseModel):
    id: Optional[int] = None
    lesson_id: Optional[int] = None 
    date: Optional[datetime.date] = None
    time: Optional[datetime.time] = None