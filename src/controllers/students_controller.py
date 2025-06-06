from dependencies import get_student_service
from fastapi import APIRouter, Depends
from src.interfaces.students.students_service_interface import IStudentService
from src.schemas.students_schema import StudentOutputSchema, StudentInputSchema, StudentUpdateInput, StudentSchemaFilter

router = APIRouter(prefix='/api/students', tags=['students'])

@router.post('/', response_model=StudentOutputSchema)
def create_student(data: StudentInputSchema, student_service: IStudentService = Depends(get_student_service)):
    return student_service.create(data)

@router.get('/{student_id}', response_model=StudentOutputSchema)
def get_student(student_id: int, student_service: IStudentService = Depends(get_student_service)):
    return student_service.get(student_id)

@router.get('/', response_model=list[StudentOutputSchema])
def list_students(filter: StudentSchemaFilter = Depends(), student_service: IStudentService = Depends(get_student_service)):
    return student_service.list(filter)

@router.put('/', response_model=StudentOutputSchema)
def update_student(data: StudentUpdateInput, student_service: IStudentService = Depends(get_student_service)):
    return student_service.update(data)

@router.delete('/{student_id}')
def delete_student(student_id: int, student_service: IStudentService = Depends(get_student_service)):
    return student_service.delete(student_id)

@router.post('/add_student_to_lesson/{student_id}/{lesson_id}')
def add_student_to_lesson(student_id: int, lesson_id: int, student_service: IStudentService = Depends(get_student_service)):
    return student_service.add_student_to_lesson(student_id, lesson_id)

