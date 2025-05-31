from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from fastapi import Depends
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from src.interfaces.authentication.authentication_utils import IAuthenticationUtils
from fastapi.exceptions import HTTPException
from fastapi import status
import config


class AuthenticationUtils(IAuthenticationUtils):

    def __init__(self):
        self.pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
        self.credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validated credentials.",
        headers={"WWW-Authenticate": "Bearer"}
        )

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        print(f'plain: {plain_password}')
        print(f'hashed: {hashed_password}')
        return self.pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
        return encoded_jwt

    def create_refresh_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(days=config.REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
        return encoded_jwt        

    def get_current_user_username(self, token: str):
        try:

            if not token:
                return None

            payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
            username: str | None = payload.get('username')
            if username is None:
                raise self.credentials_exception
            
            return username
        except JWTError:
            raise self.credentials_exception