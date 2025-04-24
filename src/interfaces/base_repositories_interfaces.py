from abc import ABC, abstractmethod
from typing import Iterable
from src.infrastructure.database import ModelType

class IBaseRepository(ABC):

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def rollback(self):
        pass

    @abstractmethod
    def flush(self):
        pass

    @abstractmethod
    def refresh(self, instance: ModelType, atributes: Iterable[str] | None = None):
        pass