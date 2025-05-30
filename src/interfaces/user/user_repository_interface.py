from abc import abstractmethod
from src.models.user import User
from src.schemas.user_schema import UserCreate
from src.schemas.user_filters import UserFilters
from src.interfaces.base_repositories_interfaces import IBaseRepository
from typing import Optional

class IUserRepository(IBaseRepository):
    
    @abstractmethod
    def get_all_users(self) -> list[User]:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> User:
        pass
    
    @abstractmethod
    def create_user(self, user: UserCreate, is_teacher: bool = True, is_adm: bool = False, company_id: Optional[int] = None) -> User:
        pass
    
    @abstractmethod
    def change_password(self, user_id: int, password: str) -> User:
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> User:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> User:
        pass

    @abstractmethod
    def get(self, filters: UserFilters) -> User:
        pass

    @abstractmethod
    def list(self, filters: UserFilters) -> list[User]:
        pass
    
    @abstractmethod
    def delete(self, user_id: int) -> User:
        pass