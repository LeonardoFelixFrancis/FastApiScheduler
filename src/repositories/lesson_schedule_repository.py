from src.interfaces.lesson_schedule_repository_interface import ILessonScheduleRepository
from src.schemas.lesson_schema import LessonScheduleFilter, LessonScheduleSchema
from src.models.lessons import LessonSchedule
from sqlalchemy.orm import Session

class LessonScheduleRepository(ILessonScheduleRepository):

    def __init__(self, db: Session):
        self.db = db

    def get(self, filter: LessonScheduleFilter) -> LessonSchedule:
        query = self._inner_list(filter)
        return query.first()
    
    def list(self, filter: LessonScheduleFilter) -> list[LessonSchedule]:
        query = self._inner_list(filter)
        return query.all()
    
    def create(self, data: LessonScheduleSchema) -> LessonSchedule:
        lesson_schedule = LessonSchedule(
            lesson_id = data.lesson_id,
            date = data.date,
            time = data.time
        )

        self.db.add(lesson_schedule)
        self.db.commit()

        return lesson_schedule
    
    def delete(self, lesson_schedule_id: int) -> bool:
        self.db.query(LessonSchedule).filter_by(id = lesson_schedule_id).delete()
        return True
    
    def update(self, data: LessonScheduleSchema) -> LessonSchedule:
        existing_lesson_schedule = self.get(LessonScheduleFilter(id = data.id))
        existing_lesson_schedule.date = data.date
        existing_lesson_schedule.time = data.time
        existing_lesson_schedule.lesson_id = data.lesson_id

        self.db.commit()
        return existing_lesson_schedule

    def _inner_list(self, filter: LessonScheduleFilter):
        query = self.db.query(LessonSchedule)

        if filter.id:
            query = query.filter(LessonSchedule.id == filter.id)

        if filter.lesson_id:
            query = query.filter(LessonSchedule.lesson_id == filter.lesson_id)

        if filter.date:
            query = query.filter(LessonSchedule.date == filter.date)

        return query