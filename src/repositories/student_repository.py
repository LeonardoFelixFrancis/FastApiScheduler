from src.interfaces.students.students_repository_interface import IStudentsRepository
from src.models.students import Student, StudentLesson
from sqlalchemy.orm import Session
from src.repositories.base_repository import BaseRepository
from src.schemas.students_schema import StudentInputSchema, StudentOutputSchema, StudentSchemaFilter, StudentUpdateInput

class StudentRepository(BaseRepository, IStudentsRepository):

    def __init__(self, db):
        super().__init__(db)

    def create(self, data: StudentInputSchema, company_id: int) -> Student:
        student = Student(**data.model_dump())
        student.company_id = company_id
        self.db.add(student)
        return student
    
    def get(self, student_id: int) -> Student | None:
        return self.db.query(Student).filter(Student.id == student_id).first()
    
    def list(self, filter: StudentSchemaFilter):
        query = self.db.query(Student)

        if filter.name:
            query = query.filter(Student.name.ilike(f'%{filter.name}%'))

        return query.all()
    
    def update(self, student: Student, data: StudentUpdateInput) -> Student:
        data_dict = data.model_dump()
        for key, value in data_dict.items():
            if key in ('id'):
                continue

            if not hasattr(student, key):
                continue

            setattr(student, key, value)

        return student
    
    def delete(self, student: Student) -> Student:
        self.db.delete(student)
        return student
    
    def add_user_to_lesson(self, lesson, student):
        new_student_lessson = StudentLesson(lesson_id = lesson.id, student_id = student.id)
        self.db.add(new_student_lessson)
        return new_student_lessson