from src.schemas.students_schema import StudentInputSchema, StudentOutputSchema, StudentSchemaFilter, StudentUpdateInput
from abc import ABC, abstractmethod

class IStudentService(ABC):

    @abstractmethod
    def create(self, data: StudentInputSchema) -> StudentOutputSchema:
        pass

    @abstractmethod
    def update(self, data: StudentUpdateInput) -> StudentOutputSchema:
        pass

    @abstractmethod
    def get(self, student_id: int) -> StudentOutputSchema:
        pass

    @abstractmethod
    def list(self, filter: StudentSchemaFilter) -> list[StudentOutputSchema]:
        pass

    @abstractmethod
    def delete(self, student_id: int) -> bool:
        pass

    @abstractmethod
    def add_student_to_lesson(self, student_id: int, lesson_id: int):
        pass