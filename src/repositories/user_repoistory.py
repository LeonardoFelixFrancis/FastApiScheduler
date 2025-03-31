from sqlalchemy.orm import Session
from src.models.user import User
from src.interfaces.authentication_utils import IAuthenticationUtils
from src.schemas.user_schema import UserCreate
from src.infrastructure.database import get_db
from fastapi import Depends
from src.interfaces.user_repository_interface import IUserRepository

class UserRepository(IUserRepository):

    def __init__(self, db: Session, authentication_utils: IAuthenticationUtils):
        self.db = db
        self.authentication_utils = authentication_utils

    def get_all_users(self):
        return self.db.query(User).all()
    
    def get_user_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()
    
    def create_user(self, user: UserCreate):
        db_user = User(
            name=user.name, 
            email=user.email, 
            username=user.username, 
            password=self.authentication_utils.hash_password(user.password)
        )

        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def get_by_username(self, username: str):
        return self.db.query(User).filter(User.username == username).first()
