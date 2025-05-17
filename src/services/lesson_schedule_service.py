from src.interfaces.lesson.lesson_schedule_service_interface import ILessonScheduleService
from src.interfaces.lesson.lesson_schedule_repository_interface import ILessonScheduleRepository
from src.interfaces.lesson.lesson_repository_interface import ILessonRepository
from src.schemas.lesson_schema import LessonScheduleFilter, LessonScheduleSchema, LessonFilter, LessonScheduleUpdateSchema
from src.models.lessons import Lesson
from src.models.user import User
from src.exceptions import (lesson_schedule_does_not_exist, 
                            unauthorized_action, 
                            lesson_does_not_exist,
                            lesson_schedule_conflict)
from datetime import timedelta

class LessonScheduleService(ILessonScheduleService):

    def __init__(self, lesson_schedule_repository: ILessonScheduleRepository, 
                 lesson_repository: ILessonRepository, 
                 logged_user: User):
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

        existing_lesson = self.lesson_repository.get(LessonFilter(id = data.lesson_id))

        if existing_lesson is None:
            raise lesson_does_not_exist
        
        if existing_lesson.company_id != self.logged_user.company_id:
            raise unauthorized_action
        
        begin_datetime = data.scheduled_at
        end_datetime = data.scheduled_at + timedelta(minutes=data.minutes_duration)

        overlaping_lesson_schedule = self.lesson_schedule_repository.get(LessonScheduleFilter(
            scheduled_at_begin = begin_datetime,
            scheduled_at_end = end_datetime,
            company_id = self.logged_user.company_id,
            teacher_id = existing_lesson.teacher_id
        ))

        if overlaping_lesson_schedule:
            raise lesson_schedule_conflict

        lesson_schedule = self.lesson_schedule_repository.create(data, self.logged_user.company_id)
        self.lesson_schedule_repository.commit()
        return lesson_schedule
    
    def update(self, data: LessonScheduleUpdateSchema) -> Lesson:
        existing_lesson_schedule = self.lesson_schedule_repository.get(LessonScheduleFilter(id = data.id, company_id=self.logged_user.company_id))

        if not existing_lesson_schedule:
            raise lesson_schedule_does_not_exist
        
        if existing_lesson_schedule.company_id != self.logged_user.company_id:
            raise unauthorized_action

        lesson_schedule_updated = self.lesson_schedule_repository.update(data)
        self.lesson_schedule_repository.commit()

        new_scheduled_at = data.scheduled_at if data.scheduled_at else existing_lesson_schedule.scheduled_at
        minutes_duration = data.minutes_duration if data.minutes_duration else existing_lesson_schedule.minutes_duration

        end_datetime = new_scheduled_at + timedelta(minutes = minutes_duration)
        overlaping_lesson_schedule = self.lesson_schedule_repository.get(LessonScheduleFilter(
            scheduled_at_begin = new_scheduled_at,
            scheduled_at_end = end_datetime,
            teacher_id = existing_lesson_schedule.lesson_info.teacher_id
        ), existing_lesson_schedule.id)

        if overlaping_lesson_schedule:
            raise lesson_schedule_conflict

        return lesson_schedule_updated
        
    def delete(self, lesson_id: int) -> bool:

        existing_lesson_schedule = self.lesson_schedule_repository.get(LessonScheduleFilter(id = lesson_id, company_id=self.logged_user.company_id))

        if not existing_lesson_schedule:
            raise lesson_schedule_does_not_exist
        
        if existing_lesson_schedule.company_id == self.logged_user.company_id:
            raise unauthorized_action

        self.lesson_schedule_repository.delete(lesson_id)
        self.lesson_schedule_repository.commit()

        return True    
