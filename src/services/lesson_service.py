from src.interfaces.lesson_service_interface import ILessonService
from src.interfaces.lesson_repository_interface import ILessonRepository
from src.interfaces.user_repository_interface import IUserRepository
from src.schemas.user_filters import UserFilters
from src.schemas.lesson_schema import LessonFilter, LessonSchema
from src.models.lessons import Lesson
from src.exceptions import teacher_does_not_exist, informed_user_is_not_teacher, lesson_does_not_exist

class LessonService(ILessonService):

    def __init__(self, lesson_repository: ILessonRepository, user_repository: IUserRepository):
        self.lesson_repository = lesson_repository
        self.user_repository = user_repository

    def get(self, filters: LessonFilter) -> Lesson:
        return self.lesson_repository.get(filters)
    
    def list(self, filters: LessonFilter) -> list[Lesson]:
        return self.lesson_repository.list(filters)
    
    def create(self, data: LessonSchema) -> Lesson:

        existing_user = self.user_repository.get(UserFilters(id = data.teacher_id))

        if existing_user is None:
            raise teacher_does_not_exist
        
        if not existing_user.is_teacher:
            raise informed_user_is_not_teacher

        return self.lesson_repository.create(data)
    
    def update(self, data: LessonSchema) -> Lesson:
        existing_user = self.user_repository.get(UserFilters(id = data.teacher_id))

        if existing_user is None:
            raise teacher_does_not_exist
        
        if not existing_user.is_teacher:
            raise informed_user_is_not_teacher
        
        existing_lesson = self.lesson_repository.get(LessonFilter(id = data.id))

        if existing_lesson is None:
            raise lesson_does_not_exist

        return self.lesson_repository.update(data)
        
    def delete(self, lesson_id: int) -> bool:
        self.lesson_repository.delete(lesson_id)
        return True    
