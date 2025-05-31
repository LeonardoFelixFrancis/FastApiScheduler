from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from src.interfaces.email.email_interface import IEmailService
from src.interfaces.authentication.authentication_service_interface import IAuthenticationService
from src.interfaces.user.user_repository_interface import IUserRepository
from src.interfaces.authentication.authentication_utils import IAuthenticationUtils
from src.interfaces.authentication.authentication_repository import IAuthenticationRepository
from src.interfaces.password_reset.password_reset_repository_interface import IPasswordResetRepository
from src.schemas.user_filters import UserFilters
from src.schemas.reset_password_schema import ResetPasswordSchema
from sqlalchemy.orm import Session
from src.schemas.login_schema import LoginSchema
from src.schemas.password_reset_schema import PasswordResetSchema
from fastapi.exceptions import HTTPException
from src.exceptions import (user_does_not_exist_forgot_password, password_reset_does_not_exists, password_and_confirm_password_are_not_equal, expired_token)
from datetime import datetime, timedelta, timezone
import uuid
import config

class AuthenticationService(IAuthenticationService):

    def __init__(self, user_repository: IUserRepository, 
                       authentication_utils: IAuthenticationUtils, 
                       email_service: IEmailService,
                       authentication_repository: IAuthenticationRepository,
                       password_reset_repository: IPasswordResetRepository
                       ):
        self.user_repository = user_repository
        self.authentication_utils = authentication_utils
        self.email_service = email_service
        self.authentication_repository = authentication_repository
        self.password_reset_repository = password_reset_repository

        self.incorrect_credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos.",
            headers={"WWW-Authenticate": "Bearer"}
        )

        self.invalid_token_exception = HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = 'No user is associated with the informed token',
            headers={'WWW-Authenticate': 'Bearer'}
        )

    def login_user(self, data: LoginSchema):
        user = self.user_repository.get_by_email(data.email)
        print(f'user {user}')

        if user is None:
            raise self.incorrect_credentials_exception
        password_check = self.authentication_utils.verify_password(data.password, user.password)
        print(f'password check {password_check}')
        if not password_check: 
            raise self.incorrect_credentials_exception
        
        access_token = self.authentication_utils.create_access_token(data={"username": user.username})
        refresh_token = self.authentication_utils.create_refresh_token(data={"username": user.username})

        return {"access_token": access_token, 
                "refresh_token": refresh_token, 
                "token_type": "bearer", 
                "user_data": {"id": user.id, "name": user.name, "username": user.username, "email": user.email}}
    
    def refresh_token(self, refresh_token: str):
        username = self.authentication_utils.get_current_user_username(refresh_token)
        user = self.user_repository.get_by_username(username)

        if not user:
            raise self.invalid_token_exception
        
        access_token = self.authentication_utils.create_access_token(data={"username": user.username})

        return {"access_token": access_token}

    def forgot_password(self, email):
        user = self.user_repository.get(UserFilters(email=email))

        if not user:
            raise user_does_not_exist_forgot_password
        
        token = str(uuid.uuid4())

        self.password_reset_repository.create(PasswordResetSchema(
            token = token,
            minutes_to_live = 60 * 24,
            user_id = user.id,
            active=True
        ))

        self.password_reset_repository.commit()
        self.email_service.send(user.email, 'forgot_password.html', {'token'})

        return True

    def reset_password(self, data: ResetPasswordSchema, token: str) -> bool:
        password_reset = self.authentication_repository.get_password_reset(token)

        if not password_reset.active:
            raise token_valid_until

        if not password_reset:
            raise password_reset_does_not_exists
        
        today = datetime.now(timezone.utc)
        token_valid_until = password_reset.created_at.replace(tzinfo=timezone.utc) + timedelta(minutes=password_reset.minutes_to_live)

        if today >= token_valid_until:
            raise expired_token

        if data.password != data.confirm_password:
            raise password_and_confirm_password_are_not_equal
        
        self.user_repository.change_password(password_reset.user_id, data.password)
        self.password_reset_repository.update(password_reset, PasswordResetSchema(token = password_reset.token,
                                                                                  minutes_to_live = password_reset.minutes_to_live,
                                                                                  created_at=password_reset.created_at,
                                                                                  user_id=password_reset.user_id, 
                                                                                  active=False))
        self.user_repository.commit()

        return True