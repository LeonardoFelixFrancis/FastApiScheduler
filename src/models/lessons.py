from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import ARRAY
from src.infrastructure.database import Base
import datetime

class Lesson(Base):
    __tablename__ = 'lessons'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    lesson_name: Mapped[str] = mapped_column(String, nullable=False)
    lesson_subject: Mapped[str] = mapped_column(String, nullable=False)
    students: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    company_id: Mapped[int | None] = mapped_column(ForeignKey("companies.id"), index=True)
    teacher = relationship("User", back_populates="lessons")
    schedules = relationship("LessonSchedule", back_populates="lesson_info")
    company = relationship("Company", back_populates="lessons")

class LessonSchedule(Base):
    __tablename__ = 'lesson_schedule'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id"), nullable=False)
    scheduled_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    minutes_duration: Mapped[int] = mapped_column(Integer, nullable=False, default=60)
    company_id: Mapped[int | None] = mapped_column(ForeignKey("companies.id"), index=True)

    lesson_info = relationship("Lesson", back_populates="schedules")
    company = relationship("Company", back_populates="schedules")