from abc import ABC, abstractmethod
from src.schemas.password_reset_schema import PasswordResetSchema
from src.models.password_reset import PasswordReset
from src.interfaces.base_repositories_interfaces import IBaseRepository

class IPasswordResetRepository(IBaseRepository):

    @abstractmethod
    def get(self, token: str) -> PasswordReset:
        pass 

    @abstractmethod
    def create(self, data: PasswordResetSchema) -> PasswordReset:
        pass
    
    @abstractmethod
    def update(self, password_reset: PasswordReset, data: PasswordResetSchema):
        pass