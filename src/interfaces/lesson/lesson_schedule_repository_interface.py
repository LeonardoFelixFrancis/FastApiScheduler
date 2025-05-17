from src.schemas.lesson_schema import LessonScheduleFilter, LessonScheduleSchema, LessonScheduleUpdateSchema
from src.models.lessons import LessonSchedule
from abc import abstractmethod
from src.interfaces.base_repositories_interfaces import IBaseRepository

class ILessonScheduleRepository(IBaseRepository):

    @abstractmethod
    def get(self, filters: LessonScheduleFilter, exclude_id: int | None = None) -> LessonSchedule:
        pass

    @abstractmethod
    def list(self, filters: LessonScheduleFilter, exclude_id: int | None = None) -> list[LessonSchedule]:
        pass
    
    @abstractmethod
    def create(self, data: LessonScheduleSchema, company_id: int | None) -> LessonSchedule:
        pass
    
    @abstractmethod
    def update(self, data: LessonScheduleUpdateSchema) -> LessonSchedule:
        pass

    @abstractmethod
    def delete(self, lesson_schedule_id: int) -> bool:
        pass