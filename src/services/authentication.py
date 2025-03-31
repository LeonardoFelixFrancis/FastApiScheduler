from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from src.interfaces.user_repository_interface import IUserRepository
from src.interfaces.authentication_utils import IAuthenticationUtils
from sqlalchemy.orm import Session
from src.schemas.login_schema import LoginSchema
from fastapi.exceptions import HTTPException
import config

class AuthenticationService:

    def __init__(self, user_repository: IUserRepository, authentication_utils: IAuthenticationUtils):
        self.user_repository = user_repository
        self.authentication_utils = authentication_utils

        self.incorrect_credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    def login_user(self, data: LoginSchema):
        user = self.user_repository.get_by_username(data.username)

        if not self.authentication_utils.verify_password(data.password, user.password):
            raise self.incorrect_credentials_exception
        
        access_token = self.authentication_utils.create_access_token(data={"username": data.username})
        refresh_token = self.authentication_utils.create_refresh_token(data={"username": data.username})

        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
    