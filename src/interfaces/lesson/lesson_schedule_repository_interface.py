from src.schemas.lesson_schema import LessonScheduleFilter, LessonScheduleSchema, LessonScheduleSchemaResponse
from src.models.lessons import LessonSchedule
from src.models.students import Student
from abc import abstractmethod
from src.interfaces.base_repositories_interfaces import IBaseRepository
from typing import List

class ILessonScheduleRepository(IBaseRepository):

    @abstractmethod
    def get(self, filters: LessonScheduleFilter) -> LessonSchedule | None:
        pass

    @abstractmethod
    def list(self, filters: LessonScheduleFilter) -> list[LessonSchedule]:
        pass
    
    @abstractmethod
    def create(self, data: LessonScheduleSchema, company_id: int | None) -> LessonSchedule:
        pass
    
    @abstractmethod
    def update(self, data: LessonScheduleSchema) -> LessonSchedule:
        pass

    @abstractmethod
    def delete(self, lesson_schedule_id: int) -> bool:
        pass
    
    @abstractmethod
    def get_schedule_attendances(self, schedule_id: int):
        pass