from abc import ABC, abstractmethod
from src.schemas.login_schema import LoginSchema
import config

class IAuthenticationService:

    @abstractmethod
    def login_user(self, data: LoginSchema):
        pass
            