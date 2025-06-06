from src.interfaces.students.students_repository_interface import IStudentsRepository
from src.interfaces.students.students_service_interface import IStudentService
from src.interfaces.lesson.lesson_repository_interface import ILessonRepository
from src.schemas.students_schema import StudentInputSchema, StudentOutputSchema, StudentSchemaFilter, StudentUpdateInput
from src.schemas.lesson_schema import LessonFilter
from src.models.user import User
from src.exceptions import student_doest_not_exists, lesson_does_not_exist, unauthorized_action
class StudentService(IStudentService):

    def __init__(self, students_repository: IStudentsRepository, lesson_repository: ILessonRepository, logged_user: User):
        self.student_repository = students_repository
        self.lesson_repository = lesson_repository
        self.logged_user = logged_user

    def create(self, data: StudentInputSchema) -> StudentOutputSchema:

        if not self.logged_user.is_adm:
            raise unauthorized_action
        
        if not self.logged_user.company_id:
            raise unauthorized_action

        student = self.student_repository.create(data, self.logged_user.company_id)
        self.student_repository.commit()
        return StudentOutputSchema.model_validate(student)
    
    def get(self, student_id: int) -> StudentOutputSchema:
        student = self.student_repository.get(student_id)

        if student is None:
            raise student_doest_not_exists

        if student.company_id != self.logged_user.company_id:
            raise unauthorized_action

        return StudentOutputSchema.model_validate(student)
    
    def list(self, filter: StudentSchemaFilter) -> list[StudentOutputSchema]:
        filter.company_id = self.logged_user.company_id
        students = self.student_repository.list(filter)
        return [StudentOutputSchema.model_validate(student) for student in students]
    
    def update(self, data: StudentUpdateInput) -> StudentOutputSchema:
        student = self.student_repository.get(data.id)

        if student is None:
            raise student_doest_not_exists
        
        if student.company_id != self.logged_user.company_id:
            raise unauthorized_action

        updated_student = self.student_repository.update(student, data)
        self.student_repository.commit()
        return StudentOutputSchema.model_validate(updated_student)
    
    def delete(self, student_id: int) -> bool:
        student = self.student_repository.get(student_id)

        if student is None:
            raise student_doest_not_exists
        
        if student.company_id != self.logged_user.company_id:
            raise unauthorized_action
        
        self.student_repository.delete(student)
        self.student_repository.commit()
        return True
    
    def add_student_to_lesson(self, student_id, lesson_id) -> None:
        student = self.student_repository.get(student_id)
        
        if student is None:
            raise student_doest_not_exists
        
        if student.company_id != self.logged_user.company_id:
            raise unauthorized_action
        
        lesson = self.lesson_repository.get(LessonFilter(id = lesson_id))

        if lesson is None:
            raise lesson_does_not_exist
        
        self.student_repository.add_user_to_lesson(lesson, student)
        self.student_repository.commit()

        return None