from sqlalchemy.orm import Session
from src.models.user import User
from src.interfaces.authentication.authentication_utils import IAuthenticationUtils
from src.schemas.user_schema import UserCreate
from src.schemas.user_filters import UserFilters
from src.infrastructure.database import get_db
from fastapi import Depends
from src.interfaces.user.user_repository_interface import IUserRepository
from src.repositories.base_repository import BaseRepository
from typing import Optional
import uuid

class UserRepository(BaseRepository, IUserRepository):

    def __init__(self, db: Session, authentication_utils: IAuthenticationUtils):
        self.authentication_utils = authentication_utils

        super().__init__(db)

    def get_all_users(self):
        return self.db.query(User).all()
    
    def get_user_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()
    
    def create_user(self, user: UserCreate, is_teacher: bool = True, is_adm: bool = False, company_id: Optional[int] = None):
        
        if not user.password:
            user.password = str(uuid.uuid4())

        db_user = User(
            name=user.name, 
            email=user.email, 
            username=user.username, 
            password=self.authentication_utils.hash_password(user.password),
        )

        db_user.is_teacher = is_teacher
        db_user.is_adm = is_adm
        db_user.company_id = company_id

        self.db.add(db_user)
        return db_user
    
    def change_password(self, user_id, password) -> User | None:
        user = self.db.query(User).filter(User.id == user_id).first()

        if user:
            user.password = self.authentication_utils.hash_password(password)
            return user

        return None
    
    def get_by_username(self, username: str):
        return self.db.query(User).filter(User.username == username).first()
    
    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()
    
    def get(self, user_filters: UserFilters) -> User:
        query = self._inner_list(user_filters)
        return query.first()
    
    def list(self, user_filters: UserFilters) -> list[User]:
        query = self._inner_list(user_filters)
        query = query.filter_by(active = True)
        return query.all()
    
    def _inner_list(self, user_filters: UserFilters):
        query = self.db.query(User)

        if user_filters.id:
            query = query.filter(User.id == user_filters.id)

        if user_filters.email:
            query = query.filter(User.email.ilike(f'%{user_filters.email}%'))

        if user_filters.username:
            query = query.filter(User.username.ilike(f'%{user_filters.username}%'))
    
        if user_filters.name:
            query = query.filter(User.name.ilike(f'%{user_filters.name}%'))

        if user_filters.is_teacher:
            query = query.filter(User.is_teacher == user_filters.is_teacher)

        return query
    
    def delete(self, user_id: int) -> User | None:
        user = self.db.query(User).filter_by(id = user_id).first()
        
        if user:
            user.active = False
            return user

        return None