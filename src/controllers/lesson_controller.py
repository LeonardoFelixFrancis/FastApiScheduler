from src.interfaces.lesson_service_interface import ILessonService
from dependencies import get_lesson_service, get_current_user
from fastapi import Depends, APIRouter
from src.schemas.lesson_schema import LessonFilter, LessonSchema
from typing import Optional


router = APIRouter('/lesson', tags=['lessons'])

@router.get('/')
def list_lessons(lesson_service: ILessonService = Depends(get_lesson_service), 
                id: Optional[int] = None,
                lesson_name: Optional[str] = None,
                lesson_subject: Optional[str] = None,
                teacher_id: Optional[int] = None
                ):
    
    return lesson_service.list(LessonFilter(id, lesson_name, lesson_subject, teacher_id))

@router.get('/{lesson_id}')
def get_lesson(lesson_id: int, lesson_service: ILessonService = Depends(get_lesson_service)):
    return lesson_service.get(LessonFilter(id = lesson_id))

@router.post('/')
def create_lesson(data: LessonSchema, lesson_service: ILessonService = Depends(get_lesson_service)):
    return lesson_service.create(data)

@router.delete('/{lesson_id}')
def delete_lesson(lesson_id: int, lesson_service: ILessonService = Depends(get_lesson_service)):
    return lesson_service.delete(lesson_id)

@router.put('/')
def update_lesson(data: LessonSchema, lesson_service: ILessonService = Depends(get_lesson_service)):
    return lesson_service.update(data)

