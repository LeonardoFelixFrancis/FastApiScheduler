from fastapi import APIRouter, Depends
from dependencies import get_authentication_service
from src.schemas.login_schema import LoginSchema
from src.schemas.refresh_schema import RefreshSchema
from src.interfaces.authentication_service_interface import IAuthenticationService
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