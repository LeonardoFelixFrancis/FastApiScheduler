from src.models.students import Student, StudentLesson
from src.models.lessons import Lesson, LessonSchedule, LessonScheduleAttendance
from src.interfaces.base_repositories_interfaces import IBaseRepository
from src.schemas.students_schema import StudentSchemaFilter, StudentInputSchema, StudentOutputSchema, StudentUpdateInput, StudentsDBResponse
from abc import ABC, abstractmethod
from typing import List
class IStudentsRepository(IBaseRepository):
    
    @abstractmethod
    def get(self, student_id: int) -> Student | None:
        pass

    @abstractmethod
    def list(self, filter: StudentSchemaFilter) -> List[Student]:
        pass
    
    @abstractmethod
    def create(self, data: StudentInputSchema, company_id: int) -> Student:
        pass

    @abstractmethod
    def update(self, student: Student, data: StudentUpdateInput) -> Student:
        pass

    @abstractmethod
    def delete(self, student: Student) -> Student:
        pass

    @abstractmethod
    def remove_user_to_lesson(self, student_ids: List[int], lesson_id: int) -> None:
        pass
    
    @abstractmethod
    def add_user_to_lesson(self, lesson: Lesson, student: Student) -> StudentLesson:
        pass

    @abstractmethod
    def get_many_by_id(self, ids: List[int], company_id: int) -> List[Student]:
        pass

    @abstractmethod
    def get_students(self, lessons: List[Lesson]) -> List[StudentsDBResponse]:
        pass

    @abstractmethod
    def get_attendances_of_schedule(self, lesson_schedule: LessonSchedule) -> List[LessonScheduleAttendance]:
        pass

    @abstractmethod
    def create_student_attendance(self, lesson_schedule: LessonSchedule, student: Student, attended: bool = False) -> LessonScheduleAttendance:
        pass

    @abstractmethod
    def get_attendance(self, lesson_schedule: LessonSchedule, student: Student):
        pass