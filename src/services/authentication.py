from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from src.interfaces.user.user_repository_interface import IUserRepository
from src.interfaces.authentication.authentication_utils import IAuthenticationUtils
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

        self.invalid_token_exception = HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = 'No user is associated with the informed token',
            headers={'WWW-Authenticate': 'Bearer'}
        )

    def login_user(self, data: LoginSchema):
        user = self.user_repository.get_by_username(data.username)

        if user is None:
            raise self.incorrect_credentials_exception

        if not self.authentication_utils.verify_password(data.password, user.password):
            raise self.incorrect_credentials_exception
        
        access_token = self.authentication_utils.create_access_token(data={"username": data.username})
        refresh_token = self.authentication_utils.create_refresh_token(data={"username": data.username})

        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
    
    def refresh_token(self, refresh_token: str):
        username = self.authentication_utils.get_current_user_username(refresh_token)
        user = self.user_repository.get_by_username(username)

        if not user:
            raise self.invalid_token_exception
        
        access_token = self.authentication_utils.create_access_token(data={"username": user.username})

        return {"access_token": access_token}
