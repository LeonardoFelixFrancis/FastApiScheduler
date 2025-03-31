from src.repositories.user_repoistory import UserRepository
from src.services.user_service import UserService
from src.services.authentication import AuthenticationService
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

# SERVICES
def get_user_service(user_repository = Depends(get_user_repository)) -> UserService:
    return UserService(user_repository)

def get_authentication_service(user_repository = Depends(get_user_repository), authentication_utils: AuthenticationUtils = Depends(get_auth_utils)):
    return AuthenticationService(user_repository, authentication_utils)

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
