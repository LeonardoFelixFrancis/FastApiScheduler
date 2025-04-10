from sqlalchemy.orm import Session
from src.interfaces.user_repository_interface import IUserRepository
from src.interfaces.user_service_interface import IUserService
from fastapi import Depends
from src.schemas.user_schema import UserCreate
from src.schemas.user_filters import UserFilters
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from src.exceptions import ambiguous_permission, duplicate_email, unauthorized_action

from src.models.user import User

class UserService(IUserService):

    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository



    def list_users(self):
        return self.user_repository.get_all_users()
    
    def get_user(self, user_id: int):
        return self.user_repository.get_user_by_id(user_id)
    
    def create_user(self, user: UserCreate, logged_user: User):

        if not logged_user.is_adm:
            raise unauthorized_action

        existing_user_email = self.user_repository.get(UserFilters(email=user.email))
        existing_user_username = self.user_repository.get(UserFilters(username=user.username))

        existing_user_response = {
            'email_already_taken': '',
            'username_already_taken': ''
        }

        if existing_user_email:
            existing_user_response["email_already_taken"] = 'This E-mail is already taken.'

        if existing_user_username:
            existing_user_response["username_already_taken"] = 'This Username is already taken.'

        if existing_user_username or existing_user_email:
            return JSONResponse(existing_user_response, status_code = 409)
        
        if user.is_teacher and user.is_adm:
            return ambiguous_permission

        return self.user_repository.create_user(user)
