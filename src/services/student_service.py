from src.interfaces.students.students_repository_interface import IStudentsRepository
from src.interfaces.students.students_service_interface import IStudentService
from src.schemas.students_schema import StudentInputSchema, StudentOutputSchema, StudentSchemaFilter

class StudentService(IStudentService):

    def __init__(self, students_repository: IStudentsRepository):
        self.student_repository = students_repository

    def create(self, data: StudentInputSchema) -> StudentOutputSchema:
        