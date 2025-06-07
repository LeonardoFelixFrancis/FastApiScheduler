from src.infrastructure.database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey, Table, Column

class Student(Base):
    __tablename__ = 'students'

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(), nullable=False)
    company_id: Mapped[int] = mapped_column(Integer(), nullable=False)

StudentLesson = Table(
    "students_lessons",
    Base.metadata,
    Column("student_id", ForeignKey("students.id"), primary_key=True),
    Column("lesson_id", ForeignKey("lessons.id"), primary_key=True),
)