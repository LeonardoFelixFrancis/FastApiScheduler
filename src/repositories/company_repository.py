from src.interfaces.company.company_repository_interface import ICompanyRepository
from src.models.company import Company
from src.schemas.company_schema import CompanySchema, CompanyFilter
from sqlalchemy.orm import Session
from src.repositories.base_repository import BaseRepository

class CompanyRepository(BaseRepository, ICompanyRepository):

    def __init__(self, db: Session):
        super().__init__(db)

    def create(self, data: CompanySchema):
        company = Company(name = data.name)
        self.db.add(company)
        return company
    
    def get(self, filters: CompanyFilter) -> Company | None:
        query = self.db.query(Company)

        if filters.id:
            query = query.filter_by(id = filters.id)

        if filters.name:
            query = query.filter_by(name = filters.name)

        return query.first()
        