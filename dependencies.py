from src.repositories.user_repoistory import UserRepository
from src.repositories.lesson_repository import LessonRepository
from src.repositories.lesson_schedule_repository import LessonScheduleRepository
from src.services.user_service import UserService
from src.services.authentication import AuthenticationService
from src.services.lesson_service import LessonService
from src.services.lesson_schedule_service import LessonScheduleService
from src.infrastructure.database import get_db
from src.utils.authentication_utils import AuthenticationUtils
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import HTTPException
from fastapi import status
from fastapi import Depends
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/internal")  

# UTILS
def get_auth_utils() -> AuthenticationUtils:
    return AuthenticationUtils()

# REPOSITORIES
def get_user_repository(db: Session = Depends(get_db), authentication_utils: AuthenticationUtils = Depends(get_auth_utils)) -> UserRepository:
    return UserRepository(db, authentication_utils)

def get_lesson_repository(db: Session = Depends(get_db)) -> LessonRepository:
    return LessonRepository(db)

def get_lesson_schedule_repository(db: Session = Depends(get_db)) -> LessonScheduleRepository:
    return LessonScheduleRepository(db) 

# SERVICES
def get_user_service(user_repository = Depends(get_user_repository)) -> UserService:
    return UserService(user_repository)

def get_authentication_service(user_repository = Depends(get_user_repository), authentication_utils: AuthenticationUtils = Depends(get_auth_utils)):
    return AuthenticationService(user_repository, authentication_utils)

def get_lesson_service(lesson_repository = Depends(get_lesson_repository), user_repository = Depends(get_user_repository)) -> LessonService:
    return LessonService(lesson_repository, user_repository)

def get_lesson_schedule_service(lesson_schedule_repository = Depends(get_lesson_schedule_repository), lesson_repository = Depends(get_lesson_repository)) -> LessonScheduleService:
    return LessonScheduleService(lesson_schedule_repository, lesson_repository)
 
# OTHERS
def get_current_user(user_repository = Depends(get_user_repository), auth_utils = Depends(get_auth_utils), token = Depends(oauth2_scheme)):
    username = auth_utils.get_current_user_username(token)
    user = user_repository.get_by_username(username)

    if not user:
        raise  HTTPException(
        selfstatus_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validated credentials.",
        headers={"WWW-Authenticate": "Bearer"}
        )
    
    return user
