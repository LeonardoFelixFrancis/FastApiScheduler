from sqlalchemy.orm import Session
from typing import Iterable
from src.infrastructure.database import ModelType

class BaseRepository:

    def __init__(self, db: Session):
        self.db = db

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()

    def flush(self):
        self.db.flush()

    def refresh(self, instance: ModelType, atributes: Iterable[str] | None = None):
        self.db.refresh(instance, atributes)