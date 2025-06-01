from sqlalchemy.orm import Session
from src.interfaces.user.user_repository_interface import IUserRepository
from src.interfaces.company.company_repository_interface import ICompanyRepository
from src.interfaces.user.user_service_interface import IUserService
from src.interfaces.email.email_interface import IEmailService
from src.interfaces.password_reset.password_reset_repository_interface import IPasswordResetRepository
from fastapi import Depends
from src.schemas.user_schema import UserCreate, AdmCreate
from src.schemas.user_filters import UserFilters
from src.schemas.company_schema import CompanySchema
from src.schemas.user_filters import UserFilters
from src.schemas.password_reset_schema import PasswordResetSchema
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from src.exceptions import ambiguous_permission, duplicate_email, unauthorized_action, teacher_does_not_exist, informed_user_is_not_teacher, email_already_taken, username_already_taken
from typing import Optional
from src.models.user import User
import uuid
import os

class UserService(IUserService):

    def __init__(self, user_repository: IUserRepository, 
                       company_repository: ICompanyRepository,
                       password_reset_repository: IPasswordResetRepository, 
                       email_service: IEmailService, 
                       logged_user: User):
        self.user_repository = user_repository
        self.company_repository = company_repository
        self.logged_user = logged_user
        self.email_service = email_service
        self.password_reset_repository = password_reset_repository

    def list_users(self, filters: UserFilters):

        if not self.logged_user.is_adm:
            raise unauthorized_action

        filters.company_id = self.logged_user.company_id
        filters.is_teacher = True
        return self.user_repository.list(filters)
    
    def get_user(self, user_id: int):
        return self.user_repository.get_user_by_id(user_id)
    
    def create_adm(self, user: AdmCreate):
        company = self.company_repository.create(CompanySchema(id = None, name = user.company_name))

        self.company_repository.commit()
        self.company_repository.refresh(company)

        user = self._create_user(UserCreate(username = user.username,
                                            name = user.name,
                                            email = user.email,
                                            password = user.password), False, True, company.id)
        
        self.user_repository.commit()

        return user
    
    def create_teacher(self, user: UserCreate, logged_user: User):
        try:
            if not logged_user.is_adm:
                raise unauthorized_action
            
            created_user = self._create_user(user, True, False, logged_user.company_id)
            self.user_repository.flush()
            self.user_repository.refresh(created_user)
            print(f'created_user {created_user}')
            
            token = str(uuid.uuid4())
            self.password_reset_repository.create(PasswordResetSchema(
                token = token,
                minutes_to_live = 60 * 72,
                user_id = created_user.id,
                active=True
            ))

            
            self.email_service.send(created_user.email, 'Primeiro acesso','first_access.html',  {'url': f'{os.getenv("FRONTEND_URL")}/reset_password/{token}', 
                                                                                                'nome':created_user.name})
            self.user_repository.commit()

            return created_user
        except Exception as e:
            self.user_repository.rollback()
            raise e

    def _create_user(self, user: UserCreate, is_teacher: bool = True, is_adm: bool = False, company_id: Optional[int] = None):
        existing_user_email = self.user_repository.get_by_email(user.email)
        existing_user_username = self.user_repository.get_by_username(user.username)

        if existing_user_email:
            raise email_already_taken

        if existing_user_username:
            raise username_already_taken
        
        created_user = self.user_repository.create_user(user, is_teacher, is_adm, company_id)
        
        return created_user

    def delete_teacher(self, teacher_id) -> bool:
        existing_teacher = self.user_repository.get(UserFilters(id=teacher_id))

        if not self.logged_user.is_adm:
            raise unauthorized_action

        if not existing_teacher:
            raise teacher_does_not_exist
        
        if existing_teacher.is_adm:
            raise informed_user_is_not_teacher
        
        if existing_teacher.company_id != self.logged_user.company_id:
            raise unauthorized_action
        
        self.user_repository.delete(teacher_id)
        self.user_repository.commit()
        return True