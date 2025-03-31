from abc import ABC, abstractmethod
from src.interfaces.user_repository_interface import IUserRepository
from src.schemas.user_schema import UserResponse
from src.schemas.user_schema import UserCreate

class IUserService:

    def __init__(self, user_repository: IUserRepository):
        pass
    
    @abstractmethod
    def list_users(self) -> list[UserResponse]:
        pass
    
    @abstractmethod
    def get_user(self, user_id: int) -> UserResponse:
        pass
    
    @abstractmethod
    def create_user(self, user: UserCreate) -> UserResponse:
        pass