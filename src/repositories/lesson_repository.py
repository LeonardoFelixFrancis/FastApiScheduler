from src.interfaces.lesson.lesson_repository_interface import ILessonRepository
from src.schemas.lesson_schema import LessonFilter, LessonSchema
from src.models.lessons import Lesson
from sqlalchemy.orm import Session
from src.repositories.base_repository import BaseRepository

class LessonRepository(BaseRepository, ILessonRepository):

    def __init__(self, db: Session):
        super().__init__(db)

    def get(self, filters: LessonFilter):
        query = self._inner_list(filters)
        return query.first()
    
    def list(self, filters: LessonFilter):
        query = self._inner_list(filters)
        return query.all()
    
    def create(self, data: LessonSchema, company_id: int | None) -> Lesson:
        lesson = Lesson(
            lesson_name = data.lesson_name,
            lesson_subject = data.lesson_subject,
            students = data.students,
            company_id = company_id
        )

        self.db.add(lesson)
        return lesson
    
    def update(self, data: LessonSchema) -> Lesson:
        existing_lesson = self.get(LessonFilter(id=data.id))
        existing_lesson.lesson_name = data.lesson_name
        existing_lesson.lesson_subject = data.lesson_subject
        existing_lesson.students = data.students
        return existing_lesson

    def delete(self, lesson_id):
        lesson = self.db.query(Lesson).filter_by(id = lesson_id).first()
        lesson.active = False
        return True

    def _inner_list(self, filters: LessonFilter):
        query = self.db.query(Lesson)

        if filters.lesson_name:
            query = query.filter(Lesson.lesson_name.ilike(f"%{filters.lesson_name}%"))

        if filters.lesson_subject:
            query = query.filter(Lesson.lesson_subject.ilike(f"%{filters.lesson_subject}%"))

        if filters.id:
            query = query.filter(Lesson.id == filters.id)

        if filters.company_id:
            query = query.filter(Lesson.company_id == filters.company_id)

        if filters.active:
            query = query.filter(Lesson.active == filters.active)

        return query
