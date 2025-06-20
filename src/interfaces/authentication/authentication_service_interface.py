from abc import ABC, abstractmethod
from src.schemas.login_schema import LoginSchema
from src.schemas.reset_password_schema import ResetPasswordSchema
import config

class IAuthenticationService:

    @abstractmethod
    def login_user(self, data: LoginSchema):
        pass

    @abstractmethod
    def refresh_token(self, refresh_token: str):
        pass

    @abstractmethod
    def forgot_password(self, email: str):
        pass

    @abstractmethod
    def reset_password(self, data: ResetPasswordSchema, token: str) -> bool:
        pass