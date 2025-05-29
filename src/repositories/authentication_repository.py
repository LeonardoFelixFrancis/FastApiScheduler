from src.interfaces.authentication.authentication_repository import IAuthenticationRepository
from src.models.password_reset import PasswordReset
from src.repositories.base_repository import BaseRepository
from sqlalchemy.orm import Session

class AuthenticationRepository(BaseRepository, IAuthenticationRepository):

    def __init__(self, db: Session):
        super().__init__(db)

    def get_password_reset(self, token: str) -> PasswordReset:
        query = self.db.query(PasswordReset).filter(PasswordReset.token == token)
        return query.first()