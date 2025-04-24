from abc import ABC, abstractmethod
from src.schemas.company_schema import CompanySchema, CompanyFilter
from src.models.company import Company

class ICompanyService(ABC):

    @abstractmethod
    def create(self, data: CompanySchema) -> Company:
        pass

    @abstractmethod
    def get(self, filters: CompanyFilter) -> Company | None:
        pass