from src.schemas.lesson_schema import LessonScheduleSchema, LessonScheduleFilter
from src.models.lessons import LessonSchedule
from abc import ABC, abstractmethod

class ILessonScheduleService(ABC):

    @abstractmethod
    def get(self, filters: LessonScheduleFilter) -> LessonSchedule:
        pass

    @abstractmethod
    def list(self, filters: LessonScheduleFilter) -> list[LessonSchedule]:
        pass

    @abstractmethod
    def create(self, data: LessonScheduleSchema) -> LessonSchedule:
        pass

    @abstractmethod
    def delete(self, lesson_schedule_id) -> bool:
        pass

    @abstractmethod
    def update(self, data: LessonScheduleSchema) -> LessonSchedule:
        pass

    
    