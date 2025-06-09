from src.interfaces.students.students_repository_interface import IStudentsRepository
from src.models.lessons import Lesson
from src.models.students import Student, StudentLesson
from sqlalchemy.orm import Session
from src.repositories.base_repository import BaseRepository
from src.schemas.students_schema import StudentInputSchema, StudentOutputSchema, StudentSchemaFilter, StudentUpdateInput, StudentsDBResponse
from typing import List

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
    
    def remove_user_to_lesson(self, student_ids: List[int], lesson_id: int) -> None:
        self.db.query(StudentLesson).filter(StudentLesson.student_id.in_(student_ids), StudentLesson.lesson_id == lesson_id).delete()
        

    def add_user_to_lesson(self, lesson, student):
        new_student_lessson = StudentLesson(lesson_id = lesson.id, student_id = student.id)
        self.db.add(new_student_lessson)
        return new_student_lessson
    
    def get_many_by_id(self, ids: List[int], company_id: int) -> List[Student]:
        query = self.db.query(Student).filter(Student.id.in_(ids), Student.company_id == company_id)
        return query.all()
        
    

    def get_students(self, lessons: List[Lesson]) -> List[StudentsDBResponse]:
        lesson_ids = [lesson.id for lesson in lessons]

        students = self.db.query(
            StudentLesson.lesson_id,
            Student.id,
            Student.name,
            Student.company_id
        ).join(Student, Student.id == StudentLesson.student_id)\
        .filter(StudentLesson.lesson_id.in_(lesson_ids)).all()

        return students