from abc import ABC, abstractmethod
from src.schemas.user_filters import UserFilters
from src.interfaces.user.user_repository_interface import IUserRepository
from src.interfaces.company.company_repository_interface import ICompanyRepository
from src.schemas.user_schema import UserResponse
from src.schemas.user_schema import UserCreate, AdmCreate
from src.models.user import User

class IUserService:

    def __init__(self, user_repository: IUserRepository, company_repository: ICompanyRepository, logged_user: User):
        pass
    
    @abstractmethod
    def list_users(self, filters: UserFilters) -> list[UserResponse]:
        pass
    
    @abstractmethod
    def get_user(self, user_id: int) -> UserResponse:
        pass
    
    @abstractmethod
    def create_adm(self, user: AdmCreate) -> UserResponse:
        pass

    @abstractmethod
    def create_teacher(self, user: UserCreate, logged_user: User) -> UserResponse:
        pass
    
    @abstractmethod
    def delete_teacher(self, teacher_id: int) -> bool:
        pass