from src.interfaces.lesson.lesson_schedule_repository_interface import ILessonScheduleRepository
from src.schemas.lesson_schema import LessonScheduleFilter, LessonScheduleSchema, LessonScheduleUpdateSchema
from src.models.lessons import LessonSchedule, Lesson
from sqlalchemy.orm import Session
from src.repositories.base_repository import BaseRepository

class LessonScheduleRepository(BaseRepository, ILessonScheduleRepository):

    def __init__(self, db: Session):
        
        super().__init__(db)


    def get(self, filter: LessonScheduleFilter, exclude_id: int | None = None) -> LessonSchedule:
        query = self._inner_list(filter)

        if exclude_id:
            query = query.filter(LessonSchedule.id != exclude_id)
        
        return query.first()
    
    def list(self, filter: LessonScheduleFilter, exclude_id: int | None = None) -> list[LessonSchedule]:
        query = self._inner_list(filter)

        if exclude_id:
            query = query.filter(LessonSchedule.id != exclude_id)

        return query.all()
    
    def create(self, data: LessonScheduleSchema, company_id: int | None) -> LessonSchedule:
        lesson_schedule = LessonSchedule(
            lesson_id = data.lesson_id,
            scheduled_at = data.scheduled_at,
            minutes_duration = data.minutes_duration,
            company_id = company_id
        )

        self.db.add(lesson_schedule)

        return lesson_schedule
    
    def delete(self, lesson_schedule_id: int) -> bool:
        self.db.query(LessonSchedule).filter_by(id = lesson_schedule_id).delete()
        return True
    
    def update(self, data: LessonScheduleUpdateSchema) -> LessonSchedule:
        existing_lesson_schedule = self.get(LessonScheduleFilter(id = data.id))
        
        if data.scheduled_at:
            existing_lesson_schedule.scheduled_at = data.scheduled_at

        if data.minutes_duration:
            existing_lesson_schedule.minutes_duration = data.minutes_duration

        self.db.commit()
        return existing_lesson_schedule

    def _inner_list(self, filter: LessonScheduleFilter):
        query = self.db.query(LessonSchedule)

        if filter.id:
            query = query.filter(LessonSchedule.id == filter.id)

        if filter.lesson_id:
            query = query.filter(LessonSchedule.lesson_id == filter.lesson_id)

        if filter.scheduled_at:
            query = query.filter(LessonSchedule.scheduled_at == filter.scheduled_at)

        if filter.company_id:
            query = query.filter(LessonSchedule.company_id == filter.company_id)

        if filter.minutes_duration:
            query = query.filter(LessonSchedule.minutes_duration == filter.minutes_duration)

        if filter.scheduled_at_begin and filter.scheduled_at_end:
            query = query.filter(LessonSchedule.scheduled_at >= filter.scheduled_at_begin,
                                 LessonSchedule.scheduled_at < filter.scheduled_at_end)
            
        if filter.teacher_id:
            query = query.join(Lesson, Lesson.id == LessonSchedule.lesson_id)\
                    .filter(Lesson.teacher_id == filter.teacher_id)

        return query