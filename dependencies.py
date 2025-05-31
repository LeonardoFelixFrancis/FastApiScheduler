from src.repositories.user_repoistory import UserRepository
from src.repositories.lesson_repository import LessonRepository
from src.repositories.lesson_schedule_repository import LessonScheduleRepository
from src.repositories.company_repository import CompanyRepository
from src.repositories.authentication_repository import AuthenticationRepository
from src.repositories.password_reset_repository import PaswordResetRepository
from src.services.user_service import UserService
from src.services.authentication import AuthenticationService
from src.services.lesson_service import LessonService
from src.services.lesson_schedule_service import LessonScheduleService
from src.services.company_service import CompanyService
from src.services.local_email_service import LocalEmailService
from src.services.hostinger_email_service import HostingerEmailService
from src.interfaces.email.email_interface import IEmailService
from src.infrastructure.database import get_db
from src.utils.authentication_utils import AuthenticationUtils
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import HTTPException
from fastapi import status
from fastapi import Depends
from sqlalchemy.orm import Session
import os

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

def get_company_repository(db: Session = Depends(get_db)) -> CompanyRepository:
    return CompanyRepository(db)

def get_authentication_repository(db: Session = Depends(get_db)) -> AuthenticationRepository:
    return AuthenticationRepository(db)

def get_password_reset_password(db: Session = Depends(get_db)) -> PaswordResetRepository:
    return PaswordResetRepository(db)

# OTHERS
def get_current_user(user_repository = Depends(get_user_repository), auth_utils = Depends(get_auth_utils), token = Depends(oauth2_scheme)):
    username = auth_utils.get_current_user_username(token)
    user = user_repository.get_by_username(username)

    return user

def authenticate(user = Depends(get_current_user)):
    if not user:
        raise  HTTPException(
        selfstatus_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validated credentials.",
        headers={"WWW-Authenticate": "Bearer"}
        )
    
    return user

# SERVICES
def get_emaii_service() -> IEmailService:
    environment = os.getenv('environment')

    if environment == 'production':
        return HostingerEmailService()
    
    if environment == 'local':
        return LocalEmailService()
    
    raise EnvironmentError('Specified environment does not exist.')

def get_user_service(user_repository = Depends(get_user_repository), 
                     company_repository = Depends(get_company_repository),
                     password_reset_repository = Depends(get_password_reset_password),
                     email_service = Depends(get_emaii_service),
                     logged_user = Depends(get_current_user)) -> UserService:
    return UserService(user_repository, company_repository, password_reset_repository, email_service, logged_user)

def get_authentication_service(user_repository = Depends(get_user_repository), 
                               authentication_repository = Depends(get_authentication_repository), 
                               password_reset_repository = Depends(get_password_reset_password),
                               authentication_utils: AuthenticationUtils = Depends(get_auth_utils),
                               mail_service = Depends(get_emaii_service)):
    return AuthenticationService(user_repository, 
                                 authentication_utils, 
                                 mail_service, 
                                 authentication_repository, 
                                 password_reset_repository)

def get_lesson_service(lesson_repository = Depends(get_lesson_repository), user_repository = Depends(get_user_repository), logged_user = Depends(get_current_user)) -> LessonService:
    return LessonService(lesson_repository, user_repository, logged_user)

def get_lesson_schedule_service(lesson_schedule_repository = Depends(get_lesson_schedule_repository), 
                                lesson_repository = Depends(get_lesson_repository),
                                user_repository = Depends(get_user_repository), 
                                logged_user = Depends(get_current_user)) -> LessonScheduleService:
    return LessonScheduleService(lesson_schedule_repository, lesson_repository, user_repository, logged_user)

def get_company_service(company_repository = Depends(get_company_repository)):
    return CompanyService(company_repository)