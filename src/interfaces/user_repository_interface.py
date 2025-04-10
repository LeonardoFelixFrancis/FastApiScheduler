from abc import ABC, abstractmethod
from src.models.user import User
from src.schemas.user_schema import UserCreate
from src.schemas.user_filters import UserFilters
from pydantic import BaseModel
from fastapi.exceptions import HTTPException


class IUserRepository(ABC):
    
    @abstractmethod
    def get_all_users(self) -> list[User]:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> User:
        pass
    
    @abstractmethod
    def create_user(self, user: UserCreate) -> User:
        pass
    
    @abstractmethod
    def get_by_username(self, username: str) -> User:
        pass

    @abstractmethod
    def get(self, filters: UserFilters) -> User:
        pass

    @abstractmethod
    def list(self, filters: UserFilters) -> list[User]:
        pass