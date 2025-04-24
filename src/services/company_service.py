from src.interfaces.company.company_repository_interface import ICompanyRepository
from src.interfaces.company.company_service_interface import ICompanyService
from src.schemas.company_schema import CompanyFilter, CompanySchema
from src.models.company import Company

class CompanyService(ICompanyService):

    def __init__(self, company_repository: ICompanyRepository):
        self.company_repository = company_repository

    def get(self, filters: CompanyFilter) -> Company | None:
        return self.company_repository.get(filters)
    
    def create(self, data: CompanySchema) -> Company:
        return self.company_repository.create(data)