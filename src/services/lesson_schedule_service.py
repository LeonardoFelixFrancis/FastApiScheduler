from src.interfaces.lesson.lesson_schedule_service_interface import ILessonScheduleService
from src.interfaces.lesson.lesson_schedule_repository_interface import ILessonScheduleRepository
from src.interfaces.lesson.lesson_repository_interface import ILessonRepository
from src.schemas.lesson_schema import LessonScheduleFilter, LessonScheduleSchema, LessonScheduleSchemaResponse
from src.schemas.user_filters import UserFilters
from src.models.lessons import Lesson
from src.models.user import User
from src.exceptions import lesson_schedule_does_not_exist, unauthorized_action, teacher_does_not_exist, informed_user_is_not_teacher, unauthorized_action
from src.interfaces.user.user_repository_interface import IUserRepository

class LessonScheduleService(ILessonScheduleService):

    def __init__(self, lesson_schedule_repository: ILessonScheduleRepository, 
                 lesson_repository: ILessonRepository, 
                 user_repository: IUserRepository,
                 logged_user: User):
        self.lesson_repository = lesson_repository
        self.lesson_schedule_repository = lesson_schedule_repository
        self.user_repository = user_repository
        self.logged_user = logged_user

    def get(self, filters: LessonScheduleFilter) -> LessonScheduleSchemaResponse:
        filters.company_id = self.logged_user.company_id

        if not self.logged_user.is_adm:
            filters.teacher_id = self.logged_user.id

        lesson_schedule = self.lesson_schedule_repository.get(filters)

        if lesson_schedule is None:
            raise lesson_schedule_does_not_exist

        return lesson_schedule
    
    def list(self, filters: LessonScheduleFilter) -> list[LessonScheduleSchemaResponse]:
        filters.company_id = self.logged_user.company_id
        
        if not self.logged_user.is_adm:
            filters.teacher_id = self.logged_user.id

        return self.lesson_schedule_repository.list(filters)
    
    def create(self, data: LessonScheduleSchema) -> Lesson:

        if not self.logged_user.is_adm:
            raise unauthorized_action

        existing_user = self.user_repository.get(UserFilters(id = data.teacher_id))

        if existing_user is None:
            raise teacher_does_not_exist
        
        if not existing_user.is_teacher:
            raise informed_user_is_not_teacher

        lesson_schedule = self.lesson_schedule_repository.create(data, self.logged_user.company_id)
        self.lesson_schedule_repository.commit()
        return lesson_schedule
    
    def update(self, data: LessonScheduleSchema) -> Lesson:

        if not self.logged_user.is_adm:
            raise unauthorized_action

        existing_user = self.user_repository.get(UserFilters(id = data.teacher_id))

        if existing_user is None:
            raise teacher_does_not_exist
        
        if not existing_user.is_teacher:
            raise informed_user_is_not_teacher

        existing_lesson_schedule = self.lesson_schedule_repository.get(LessonScheduleFilter(id = data.id, company_id=self.logged_user.company_id))

        if not existing_lesson_schedule:
            raise lesson_schedule_does_not_exist
        
        if existing_lesson_schedule.company_id != self.logged_user.company_id:
            raise unauthorized_action

        lesson_schedule_updated = self.lesson_schedule_repository.update(data)
        self.lesson_schedule_repository.commit()

        return lesson_schedule_updated
        
    def delete(self, lesson_id: int) -> bool:

        existing_lesson_schedule = self.lesson_schedule_repository.get(LessonScheduleFilter(id = lesson_id, company_id=self.logged_user.company_id))

        if not existing_lesson_schedule:
            raise lesson_schedule_does_not_exist
        
        if existing_lesson_schedule.company_id != self.logged_user.company_id:
            raise unauthorized_action

        self.lesson_schedule_repository.delete(lesson_id)
        self.lesson_schedule_repository.commit()

        return True    
