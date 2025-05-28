from src.interfaces.lesson.lesson_schedule_repository_interface import ILessonScheduleRepository
from src.schemas.lesson_schema import LessonScheduleFilter, LessonScheduleSchema, LessonScheduleSchemaResponse
from src.models.lessons import LessonSchedule
from sqlalchemy.orm import Session
from src.repositories.base_repository import BaseRepository
from src.models.user import User
from src.models.lessons import Lesson
class LessonScheduleRepository(BaseRepository, ILessonScheduleRepository):

    def __init__(self, db: Session):
        
        super().__init__(db)


    def get(self, filter: LessonScheduleFilter) -> LessonSchedule:
        query = self._inner_list(filter)
        item = query.first()
        if item:
            return LessonScheduleSchemaResponse(**item._asdict())
        return None
    
    def list(self, filter: LessonScheduleFilter) -> list[LessonSchedule]:
        query = self._inner_list(filter)
        items = query.all()
        return [LessonScheduleSchemaResponse(**row._asdict()) for row in items]
    
    def create(self, data: LessonScheduleSchema, company_id: int | None) -> LessonSchedule:
        lesson_schedule = LessonSchedule(
            lesson_id = data.lesson_id,
            date = data.date,
            time = data.time,
            company_id = company_id,
            teacher_id = data.teacher_id
        )

        self.db.add(lesson_schedule)

        return lesson_schedule
    
    def delete(self, lesson_schedule_id: int) -> bool:
        self.db.query(LessonSchedule).filter_by(id = lesson_schedule_id).delete()
        return True
    
    def update(self, data: LessonScheduleSchema) -> LessonSchedule:
        existing_lesson_schedule = self.db.query(LessonSchedule).filter_by(id = data.id).first()
        existing_lesson_schedule.date = data.date
        existing_lesson_schedule.time = data.time
        existing_lesson_schedule.lesson_id = data.lesson_id
        existing_lesson_schedule.teacher_id = data.teacher_id

        return existing_lesson_schedule

    def _inner_list(self, filter: LessonScheduleFilter):
        query = self.db.query(LessonSchedule.id,
                              LessonSchedule.lesson_id,
                              LessonSchedule.teacher_id,
                              LessonSchedule.lesson_info,
                              LessonSchedule.date,
                              LessonSchedule.time,
                              LessonSchedule.company_id,
                              User.name.label('teacher_name'),
                              User.active.label('teacher_active'),
                              Lesson.lesson_name,
                              Lesson.active.label('lesson_active'))\
                              .join(User, User.id == LessonSchedule.teacher_id)\
                              .join(Lesson, Lesson.id == LessonSchedule.lesson_id)

        if filter.id:
            query = query.filter(LessonSchedule.id == filter.id)

        if filter.lesson_id:
            query = query.filter(LessonSchedule.lesson_id == filter.lesson_id)

        if filter.date:
            query = query.filter(LessonSchedule.date == filter.date)

        if filter.company_id:
            query = query.filter(LessonSchedule.company_id == filter.company_id)

        if filter.teacher_id:
            query = query.filter(LessonSchedule.teacher_id == filter.teacher_id)
        
        if filter.date_start:
            query = query.filter(LessonSchedule.date >= filter.date_start)

        if filter.date_end:
            query = query.filter(LessonSchedule.date <= filter.date_end)

        return query