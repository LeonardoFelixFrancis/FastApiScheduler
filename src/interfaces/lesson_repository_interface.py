from src.models.lessons import Lesson, LessonSchedule
from src.schemas.lesson_schema import LessonFilter, LessonSchema
from abc import ABC, abstractmethod

class ILessonRepository(ABC):

    @abstractmethod
    def get(self, filters: LessonFilter) -> Lesson: 
        pass

    @abstractmethod
    def list(self, filters: LessonFilter) -> list[Lesson]:
        pass

    @abstractmethod
    def create(self, data: LessonSchema) -> Lesson: 
        pass

    @abstractmethod
    def delete(self, lesson_id: int) -> bool:
        pass

    @abstractmethod
    def update(self, data: LessonSchema) -> Lesson:
        pass

    
