from sqlalchemy.orm import Session
from src.interfaces.user.user_repository_interface import IUserRepository
from src.interfaces.company.company_repository_interface import ICompanyRepository
from src.interfaces.user.user_service_interface import IUserService
from fastapi import Depends
from src.schemas.user_schema import UserCreate, AdmCreate
from src.schemas.user_filters import UserFilters
from src.schemas.company_schema import CompanySchema
from src.schemas.user_filters import UserFilters
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from src.exceptions import ambiguous_permission, duplicate_email, unauthorized_action
from typing import Optional

from src.models.user import User

class UserService(IUserService):

    def __init__(self, user_repository: IUserRepository, company_repository: ICompanyRepository):
        self.user_repository = user_repository
        self.company_repository = company_repository

    def list_users(self, filters: UserFilters):
        return self.user_repository.list(filters)
    
    def get_user(self, user_id: int):
        return self.user_repository.get_user_by_id(user_id)
    
    def create_adm(self, user: AdmCreate):
        company = self.company_repository.create(CompanySchema(id = None, name = user.company_name))

        self.company_repository.commit()
        self.company_repository.refresh(company)

        return self._create_user(UserCreate(username = user.username,
                                            name = user.name,
                                            email = user.email,
                                            password = user.email), False, True, company.id)
    
    def create_teacher(self, user: UserCreate, logged_user: User):
        if not logged_user.is_adm:
            raise unauthorized_action
        
        return self._create_user(user, True, False, logged_user.company_id)

    def _create_user(self, user: UserCreate, is_teacher: bool = True, is_adm: bool = False, company_id: Optional[int] = None):
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
        
        created_user = self.user_repository.create_user(user, is_teacher, is_adm, company_id)
        self.user_repository.commit()
        
        return created_user
