from src.models.students import Student, StudentLesson
from src.models.lessons import Lesson
from src.interfaces.base_repositories_interfaces import IBaseRepository
from src.schemas.students_schema import StudentSchemaFilter, StudentInputSchema, StudentOutputSchema, StudentUpdateInput
from abc import ABC, abstractmethod

class IStudentsRepository(IBaseRepository):
    
    @abstractmethod
    def get(self, student_id: int) -> Student | None:
        pass

    @abstractmethod
    def list(self, filter: StudentSchemaFilter) -> list[Student]:
        pass
    
    @abstractmethod
    def create(self, data: StudentInputSchema, company_id: int) -> Student:
        pass

    @abstractmethod
    def update(self, student: Student, data: StudentUpdateInput) -> Student:
        pass

    @abstractmethod
    def delete(self, student: Student) -> Student:
        pass
    
    @abstractmethod
    def add_user_to_lesson(self, lesson: Lesson, student: Student) -> StudentLesson:
        pass