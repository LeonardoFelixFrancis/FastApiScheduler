from abc import ABC, abstractmethod
from src.models.password_reset import PasswordReset

class IAuthenticationRepository(ABC):

    @abstractmethod
    def get_password_reset(self, token: str) -> PasswordReset | None:
        pass