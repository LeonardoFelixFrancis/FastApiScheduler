from src.infrastructure.database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey

class Student(Base):
    __tablename__ = 'students'

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(), nullable=False)
    company_id: Mapped[int] = mapped_column(Integer(), nullable=False)

class StudentLesson(Base):
    __tablename__ = 'students_lessons'

    student_id = mapped_column(ForeignKey('students.id'), primary_key=True)
    lesson_id = mapped_column(ForeignKey('lessons.id'), primary_key=True)