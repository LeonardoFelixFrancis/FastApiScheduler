from abc import ABC, abstractmethod
from typing import Optional
from datetime import timedelta

class IAuthenticationUtils:

    @abstractmethod
    def hash_password(self, password: str) -> str:
       pass

    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        pass
    
    @abstractmethod
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        pass

    @abstractmethod
    def create_refresh_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        pass

    @abstractmethod
    def get_current_user_username(self, token: str):
        pass