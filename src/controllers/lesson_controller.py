from src.interfaces.lesson_service_interface import ILessonService
from dependencies import get_lesson_service, authenticate
from fastapi import Depends, APIRouter
from src.schemas.lesson_schema import LessonFilter, LessonSchema
from typing import Optional


router = APIRouter(prefix='/lesson', tags=['lessons'])

@router.get('/')
def list_lessons(lesson_service: ILessonService = Depends(get_lesson_service), 
                 user = Depends(authenticate),
                id: Optional[int] = None,
                lesson_name: Optional[str] = None,
                lesson_subject: Optional[str] = None,
                teacher_id: Optional[int] = None
                ):
    
    return lesson_service.list(LessonFilter(id=id, lesson_name=lesson_name, lesson_subject=lesson_subject, teacher_id=teacher_id))

@router.get('/{lesson_id}')
def get_lesson(lesson_id: int, lesson_service: ILessonService = Depends(get_lesson_service),
               user = Depends(authenticate)):
    return lesson_service.get(LessonFilter(id = lesson_id))

@router.post('/')
def create_lesson(data: LessonSchema, lesson_service: ILessonService = Depends(get_lesson_service),user = Depends(authenticate)):
    return lesson_service.create(data)

@router.delete('/{lesson_id}')
def delete_lesson(lesson_id: int, lesson_service: ILessonService = Depends(get_lesson_service), user = Depends(authenticate)):
    return lesson_service.delete(lesson_id)

@router.put('/')
def update_lesson(data: LessonSchema, lesson_service: ILessonService = Depends(get_lesson_service), user = Depends(authenticate)):
    return lesson_service.update(data)

