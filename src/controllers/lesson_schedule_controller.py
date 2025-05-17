from fastapi import APIRouter, Depends
from dependencies import get_lesson_schedule_service, authenticate
from src.schemas.lesson_schema import LessonScheduleFilter, LessonScheduleSchema
from src.interfaces.lesson.lesson_schedule_service_interface import ILessonScheduleService, LessonScheduleSchema
import datetime
from typing import Optional

router = APIRouter(prefix='/lesson_schedule', tags=['lesson_schedules'])

@router.get('/')
def list_lesson_schedule(lessson_schedule_service: ILessonScheduleService = Depends(get_lesson_schedule_service), 
                         user = Depends(authenticate),
                         id: Optional[int] = None,
                         lesson_id: Optional[int] = None,
                         date: Optional[datetime.date] = None,
                         time: Optional[datetime.time] = None
                        ):
    return lessson_schedule_service.list(LessonScheduleFilter(id=id, lesson_id=lesson_id, date=date, time=time))

@router.get('/')
def get_lesson_schedule(lesson_schedule_service: ILessonScheduleService = Depends(get_lesson_schedule_service),user = Depends(authenticate), id: Optional[int] = None):
    return lesson_schedule_service.get(LessonScheduleFilter(id=id))

@router.post('/')
def create_lesson_schedule(data: LessonScheduleSchema, lesson_schedule_service: ILessonScheduleService = Depends(get_lesson_schedule_service),user = Depends(authenticate),):
    return lesson_schedule_service.create(data)

@router.delete('/{lesson_schedule_id}')
def delete_lesson_schedule(lesson_schedule_id: int, lesson_schedule_service: ILessonScheduleService = Depends(get_lesson_schedule_service), user = Depends(authenticate)):
    return lesson_schedule_service.delete(lesson_schedule_id)

@router.put('/')
def update_lesson_schedule(data: LessonScheduleSchema, lesson_schedule_service: ILessonScheduleService = Depends(get_lesson_schedule_service), user = Depends(authenticate)):
    return lesson_schedule_service.update(data)