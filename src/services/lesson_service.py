from src.interfaces.lesson.lesson_service_interface import ILessonService
from src.interfaces.lesson.lesson_repository_interface import ILessonRepository
from src.interfaces.user.user_repository_interface import IUserRepository
from src.interfaces.students.students_repository_interface import IStudentsRepository
from src.schemas.user_filters import UserFilters
from src.schemas.lesson_schema import LessonFilter, LessonSchema, LessonOutput
from src.schemas.students_schema import StudentOutputSchema
from src.models.lessons import Lesson
from src.models.user import User
from src.exceptions import teacher_does_not_exist, informed_user_is_not_teacher, lesson_does_not_exist, unauthorized_action
from collections import defaultdict

class LessonService(ILessonService):

    def __init__(self, lesson_repository: ILessonRepository, 
                       user_repository: IUserRepository,
                       student_repository: IStudentsRepository,
                       logged_user: User):
        self.lesson_repository = lesson_repository
        self.user_repository = user_repository
        self.student_repository = student_repository
        self.logged_user = logged_user

    def get(self, filters: LessonFilter) -> LessonOutput:
        filters.company_id = self.logged_user.company_id
        lesson = self.lesson_repository.get(filters)
        students = self.student_repository.get_students([lesson])

        students_hash = defaultdict(list)
        for student in students:
            students_hash[student.lesson_id].append(student)
        
        lesson_students = students_hash[lesson.id]
        new_lesson = LessonOutput(
            id = lesson.id,
            lesson_name = lesson.lesson_name,
            lesson_subject = lesson.lesson_subject,
            students = [StudentOutputSchema(
                id = student.id,
                name = student.name,
                company_id = student.company_id
            ) for student in lesson_students]
        )

        return new_lesson
    
    def list(self, filters: LessonFilter) -> list[LessonOutput]:

        if not self.logged_user.is_adm:
            raise unauthorized_action

        filters.company_id = self.logged_user.company_id
        filters.active = True
        lessons = self.lesson_repository.list(filters)
        students = self.student_repository.get_students(lessons)

        students_hash = defaultdict(list)
        for student in students:
            students_hash[student.lesson_id].append(student)

        lessons_response = []
        for lesson in lessons:
            lesson_students = students_hash[lesson.id]
            new_lesson = LessonOutput(
                id = lesson.id,
                lesson_name = lesson.lesson_name,
                lesson_subject = lesson.lesson_subject,
                students = [StudentOutputSchema(
                    id = student.id,
                    name = student.name,
                    company_id = student.company_id
                ) for student in lesson_students]
            )
            lessons_response.append(new_lesson)

        return lessons_response

    
    def create(self, data: LessonSchema) -> Lesson:   

        if not self.logged_user.is_adm:
            raise unauthorized_action

        students_ids = data.students
        data.students = None

        lesson = self.lesson_repository.create(data, self.logged_user.company_id)
        self.lesson_repository.flush()

        if students_ids and self.logged_user.company_id:
            students = self.student_repository.get_many_by_id(students_ids, self.logged_user.company_id)

            for student in students:
                self.student_repository.add_user_to_lesson(lesson ,student)
    
        self.lesson_repository.commit()
        return lesson
    
    def update(self, data: LessonSchema) -> Lesson:

        if not self.logged_user.is_adm:
            raise unauthorized_action


        existing_lesson = self.lesson_repository.get(LessonFilter(id = data.id, company_id=self.logged_user.company_id))

        if existing_lesson is None:
            raise lesson_does_not_exist
        
        if existing_lesson.company_id != self.logged_user.company_id:
            raise unauthorized_action
        
        students_ids = data.students
        data.students = None
        current_students = self.student_repository.get_students([existing_lesson])
        current_students_ids = [student.id for student in current_students]

        if students_ids:
            removed_students = [student.id for student in current_students if student.id not in students_ids]

        self.student_repository.remove_user_to_lesson(removed_students, existing_lesson.id)

        if students_ids:
            added_students = [student_id for student_id in students_ids if student_id not in current_students_ids]
        
        if added_students and self.logged_user.company_id:
            students = self.student_repository.get_many_by_id(added_students, self.logged_user.company_id)

            for student in students:
                self.student_repository.add_user_to_lesson(existing_lesson ,student)
            
        
        update_lesson = self.lesson_repository.update(data)
        self.lesson_repository.commit()

        return update_lesson
        
    def delete(self, lesson_id: int) -> bool:

        if not self.logged_user.is_adm:
            raise unauthorized_action

        existing_lesson = self.lesson_repository.get(LessonFilter(id = lesson_id, company_id=self.logged_user.company_id))

        if existing_lesson is None:
            raise lesson_does_not_exist
        
        if existing_lesson.company_id != self.logged_user.company_id:
            raise unauthorized_action

        self.lesson_repository.delete(lesson_id)
        self.lesson_repository.commit()

        return True    
