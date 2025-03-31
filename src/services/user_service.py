from sqlalchemy.orm import Session
from src.interfaces.user_repository_interface import IUserRepository
from src.interfaces.user_service_interface import IUserService
from fastapi import Depends
from src.schemas.user_schema import UserCreate

class UserService(IUserService):

    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def list_users(self):
        return self.user_repository.get_all_users()
    
    def get_user(self, user_id: int):
        return self.user_repository.get_user_by_id(user_id)
    
    def create_user(self, user: UserCreate):
        return self.user_repository.create_user(user)