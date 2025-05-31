from src.repositories.base_repository import BaseRepository
from src.interfaces.password_reset.password_reset_repository_interface import IPasswordResetRepository
from src.schemas.password_reset_schema import PasswordResetSchema
from src.models.password_reset import PasswordReset
from sqlalchemy.orm import Session

class PaswordResetRepository(BaseRepository, IPasswordResetRepository):

    def __init__(self, db: Session):
        self.db = db

    def create(self, data: PasswordResetSchema) -> PasswordReset:
        new_password_reset = PasswordReset(**data.model_dump())
        self.db.add(new_password_reset)
        return new_password_reset
    
    def get(self, token: str) -> PasswordReset | None:
        password_reset = self.db.query(PasswordReset).filter(PasswordReset.token == token).first()
        return password_reset

    def update(self, password_reset: PasswordReset, data: PasswordResetSchema) -> PasswordReset:
        data = data.model_dump()

        for key, value in data.items():

            if key == 'id':
                continue

            if hasattr(password_reset, key):
                setattr(password_reset, key, value)
        
        return password_reset
        