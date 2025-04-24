from src.models.company import Company
from src.schemas.company_schema import CompanySchema, CompanyFilter
from src.interfaces.base_repositories_interfaces import IBaseRepository
from abc import abstractmethod

class ICompanyRepository(IBaseRepository):

    @abstractmethod
    def create(self, data: CompanySchema) -> Company:
        pass

    @abstractmethod
    def get(self, filters: CompanyFilter) -> Company | None:
        pass
