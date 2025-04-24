from fastapi import APIRouter, Depends
from src.schemas.user_schema import UserResponse, UserCreate
from src.interfaces.user.user_service_interface import IUserService
from dependencies import get_user_service, authenticate


router = APIRouter(prefix="/users", tags=["Users"])

@router.get('/', response_model=list[UserResponse])
def get_users(user = Depends(authenticate), user_service: IUserService = Depends(get_user_service)):
    return user_service.list_users()

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, user = Depends(authenticate), user_service: IUserService = Depends(get_user_service)):
    return user_service.get_user(user_id)

@router.post("/", response_model=UserResponse)
def create_user(user_data: UserCreate, user = Depends(authenticate), user_service: IUserService = Depends(get_user_service)):
    return user_service.create_teacher(user_data, user)
