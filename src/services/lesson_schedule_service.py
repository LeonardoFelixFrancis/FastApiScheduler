from src.interfaces.lesson_schedule_service_interface import ILessonScheduleService
from src.interfaces.lesson_schedule_repository_interface import ILessonScheduleRepository
from src.interfaces.lesson_repository_interface import ILessonRepository
from src.schemas.lesson_schema import LessonScheduleFilter, LessonScheduleSchema, LessonFilter
from src.models.lessons import Lesson

class LessonScheduleService(ILessonScheduleService):

    def __init__(self, lesson_schedule_repository: ILessonScheduleRepository, lesson_repository: ILessonRepository):
        self.lesson_repository = lesson_repository
        self.lesson_schedule_repository = lesson_schedule_repository

    def get(self, filters: LessonScheduleFilter) -> Lesson:
        return self.lesson_schedule_repository.get(filters)
    
    def list(self, filters: LessonScheduleFilter) -> list[Lesson]:
        return self.lesson_schedule_repository.list(filters)
    
    def create(self, data: LessonScheduleSchema) -> Lesson:
        return self.lesson_schedule_repository.create(data)
    
    def update(self, data: LessonScheduleSchema) -> Lesson:
        return self.lesson_schedule_repository.update(data)
        
    def delete(self, lesson_id: int) -> bool:
        self.lesson_schedule_repository.delete(lesson_id)
        return True    
