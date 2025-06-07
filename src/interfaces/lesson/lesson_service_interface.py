from src.schemas.lesson_schema import LessonSchema, LessonFilter, LessonOutput
from src.models.lessons import Lesson
from abc import ABC, abstractmethod

class ILessonService(ABC):

    @abstractmethod
    def get(self, filters: LessonFilter) -> Lesson:
        pass
    
    @abstractmethod
    def list(self, filters: LessonFilter) -> list[LessonOutput]:
        pass
    
    @abstractmethod
    def create(self, data: LessonSchema) -> Lesson:
        pass

    @abstractmethod
    def delete(self, lesson_id) -> bool:
        pass

    @abstractmethod
    def update(self, data: LessonSchema) -> Lesson:
        pass
