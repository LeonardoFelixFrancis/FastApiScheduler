from src.schemas.students_schema import StudentInputSchema, StudentOutputSchema, StudentSchemaFilter

class IStudentService:

    def create(self, data: StudentInputSchema) -> StudentOutputSchema:
        pass

    def update(self, data: StudentInputSchema) -> StudentOutputSchema:
        pass

    def get(self, student_id: int) -> StudentOutputSchema:
        pass

    def list(self, filter: StudentSchemaFilter) -> list[StudentOutputSchema]:
        pass

    def delete(self, student_id: int) -> bool:
        pass

    def add_user_to_lesson(self, student_id: int, lesson_id: int):
        pass