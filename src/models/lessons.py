from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, ForeignKey, Date, Time
from sqlalchemy.dialects.postgresql import ARRAY
from src.infrastructure.database import Base
import datetime

class Lesson(Base):
    __tablename__ = 'lessons'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    lesson_name: Mapped[str] = mapped_column(String, nullable=False)
    lesson_subject: Mapped[str] = mapped_column(String, nullable=False)
    company_id: Mapped[int | None] = mapped_column(Integer, index=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    schedules = relationship("LessonSchedule", back_populates="lesson_info")

class LessonSchedule(Base):
    __tablename__ = 'lesson_schedule'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id"), nullable=False)
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    time: Mapped[datetime.time] = mapped_column(Time, nullable=False)
    company_id: Mapped[int | None] = mapped_column(Integer, index=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    lesson_info = relationship("Lesson", back_populates="schedules")

class LessonScheduleAttendance(Base):
    __tablename__ = 'lesson_schedule_attendance'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    schedule_id: Mapped[int] = mapped_column(ForeignKey('lesson_schedule.id'), nullable = False)
    student_id: Mapped[int] = mapped_column(ForeignKey('students.id'), nullable = False)
    attended: Mapped[bool] = mapped_column(Boolean, nullable = False)