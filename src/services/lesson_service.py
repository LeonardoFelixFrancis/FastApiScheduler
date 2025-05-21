from src.interfaces.lesson.lesson_service_interface import ILessonService
from src.interfaces.lesson.lesson_repository_interface import ILessonRepository
from src.interfaces.user.user_repository_interface import IUserRepository
from src.schemas.user_filters import UserFilters
from src.schemas.lesson_schema import LessonFilter, LessonSchema
from src.models.lessons import Lesson
from src.models.user import User
from src.exceptions import teacher_does_not_exist, informed_user_is_not_teacher, lesson_does_not_exist, unauthorized_action

class LessonService(ILessonService):

    def __init__(self, lesson_repository: ILessonRepository, user_repository: IUserRepository, logged_user: User):
        self.lesson_repository = lesson_repository
        self.user_repository = user_repository
        self.logged_user = logged_user

    def get(self, filters: LessonFilter) -> Lesson:
        filters.company_id = self.logged_user.company_id
        return self.lesson_repository.get(filters)
    
    def list(self, filters: LessonFilter) -> list[Lesson]:
        filters.company_id = self.logged_user.company_id
        return self.lesson_repository.list(filters)
    
    def create(self, data: LessonSchema) -> Lesson:        
        lesson = self.lesson_repository.create(data, self.logged_user.company_id)
        self.lesson_repository.commit()
        return lesson
    
    def update(self, data: LessonSchema) -> Lesson:
        existing_lesson = self.lesson_repository.get(LessonFilter(id = data.id, company_id=self.logged_user.company_id))

        if existing_lesson is None:
            raise lesson_does_not_exist
        
        if existing_lesson.company_id != self.logged_user.company_id:
            raise unauthorized_action
        
        update_lesson = self.lesson_repository.update(data)
        self.lesson_repository.commit()

        return update_lesson
        
    def delete(self, lesson_id: int) -> bool:
        existing_lesson = self.lesson_repository.get(LessonFilter(id = lesson_id, company_id=self.logged_user.company_id))

        if existing_lesson is None:
            raise lesson_does_not_exist
        
        if existing_lesson.company_id != self.logged_user.company_id:
            raise unauthorized_action

        self.lesson_repository.delete(lesson_id)
        self.lesson_repository.commit()

        return True    
