from fastapi import APIRouter, Depends
from dependencies import get_authentication_service, get_user_service
from src.schemas.login_schema import LoginSchema
from src.schemas.refresh_schema import RefreshSchema
from src.schemas.user_schema import UserCreate, AdmCreate
from src.schemas.reset_password_schema import ResetPasswordSchema
from src.schemas.forgot_password_schema import ForgotPasswordSchema
from src.interfaces.user.user_service_interface import IUserService
from src.interfaces.authentication.authentication_service_interface import IAuthenticationService
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(prefix='/auth', tags=['auth'])

@router.post('/login')
def login(data: LoginSchema, auth_service: IAuthenticationService = Depends(get_authentication_service)):
    return auth_service.login_user(data)

@router.post('/refresh')
def refresh(refresh_data: RefreshSchema, auth_service: IAuthenticationService = Depends(get_authentication_service)):
    return auth_service.refresh_token(refresh_data.refresh_token)

@router.post('/internal')
def internal_login(data: OAuth2PasswordRequestForm = Depends(), auth_service: IAuthenticationService = Depends(get_authentication_service)):
    return auth_service.login_user(LoginSchema(**{"username": data.username, "password": data.password}))

@router.post('/register')
def register(data: AdmCreate, user_service: IUserService = Depends(get_user_service)):
    return user_service.create_adm(data)

@router.post('/reset_password/{token}')
def reset_password(token: str, data: ResetPasswordSchema, auth_service: IAuthenticationService = Depends(get_authentication_service)):
    return auth_service.reset_password(data, token)

@router.post('/forgot_password')
def forgot_password(data: ForgotPasswordSchema, auth_service: IAuthenticationService = Depends(get_authentication_service)):
    return auth_service.forgot_password(data.email)