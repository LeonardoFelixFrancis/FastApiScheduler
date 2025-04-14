from src.interfaces.lesson_repository_interface import ILessonRepository
from src.schemas.lesson_schema import LessonFilter, LessonSchema
from src.models.lessons import Lesson
from sqlalchemy.orm import Session

class LessonRepository(ILessonRepository):

    def __init__(self, db: Session):
        self.db = db

    def get(self, filters: LessonFilter):
        query = self._inner_list(filters)
        return query.first()
    
    def list(self, filters: LessonFilter):
        query = self._inner_list(filters)
        return query.all()
    
    def create(self, data: LessonSchema, company_id: int) -> Lesson:
        lesson = Lesson(
            lesson_name = data.lesson_name,
            lesson_subject = data.lesson_subject,
            students = data.students,
            teacher_id = data.teacher_id,
            company_id = company_id
        )

        self.db.add(lesson)
        self.db.commit()

        return lesson
    
    def update(self, data: LessonSchema) -> Lesson:
        existing_lesson = self.get(LessonFilter(id=data.id))
        existing_lesson.lesson_name = data.lesson_name
        existing_lesson.lesson_subject = data.lesson_subject
        existing_lesson.students = data.students
        existing_lesson.teacher_id = data.teacher_id

        self.db.commit()
        return existing_lesson

    def delete(self, lesson_id):
        self.db.query(Lesson).filter_by(id = lesson_id).delete()
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

        return query
