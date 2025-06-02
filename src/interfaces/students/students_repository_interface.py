from src.models.students import Student, StudentLesson
from src.models.lessons import Lesson
from src.interfaces.base_repositories_interfaces import IBaseRepository
from src.schemas.students_schema import StudentSchemaFilter, StudentInputSchema, StudentOutputSchema

class IStudentsRepository(IBaseRepository):
    
    def get(self, student_id: int) -> Student:
        pass

    def list(self, filter: StudentSchemaFilter) -> list[Student]:
        pass

    def create(self, data: StudentInputSchema) -> Student:
        pass

    def update(self, student: Student, data: StudentInputSchema) -> Student:
        pass

    def delete(self, student: Student) -> None:
        pass
    
    def add_user_to_lesson(self, lesson: Lesson, student: Student) -> StudentLesson:
        pass