from src.interfaces.lesson_schedule_service_interface import ILessonScheduleService
from src.interfaces.lesson_schedule_repository_interface import ILessonScheduleRepository
from src.interfaces.lesson_repository_interface import ILessonRepository
from src.schemas.lesson_schema import LessonScheduleFilter, LessonScheduleSchema, LessonFilter
from src.models.lessons import Lesson
from src.models.user import User
from src.exceptions import lesson_schedule_does_not_exist, unauthorized_action

class LessonScheduleService(ILessonScheduleService):

    def __init__(self, lesson_schedule_repository: ILessonScheduleRepository, lesson_repository: ILessonRepository, logged_user: User):
        self.lesson_repository = lesson_repository
        self.lesson_schedule_repository = lesson_schedule_repository
        self.logged_user = logged_user

    def get(self, filters: LessonScheduleFilter) -> Lesson:
        filters.company_id = self.logged_user.company_id
        return self.lesson_schedule_repository.get(filters)
    
    def list(self, filters: LessonScheduleFilter) -> list[Lesson]:
        filters.company_id = self.logged_user.company_id
        return self.lesson_schedule_repository.list(filters)
    
    def create(self, data: LessonScheduleSchema) -> Lesson:
        return self.lesson_schedule_repository.create(data, self.logged_user.company_id)
    
    def update(self, data: LessonScheduleSchema) -> Lesson:
        existing_lesson_schedule = self.lesson_schedule_repository.get(LessonScheduleFilter(id = data.id, company_id=self.logged_user.company_id))

        if not existing_lesson_schedule:
            raise lesson_schedule_does_not_exist
        
        if existing_lesson_schedule.company_id == self.logged_user.company_id:
            raise unauthorized_action

        return self.lesson_schedule_repository.update(data)
        
    def delete(self, lesson_id: int) -> bool:

        existing_lesson_schedule = self.lesson_schedule_repository.get(LessonScheduleFilter(id = lesson_id, company_id=self.logged_user.company_id))

        if not existing_lesson_schedule:
            raise lesson_schedule_does_not_exist
        
        if existing_lesson_schedule.company_id == self.logged_user.company_id:
            raise unauthorized_action

        self.lesson_schedule_repository.delete(lesson_id)
        return True    
