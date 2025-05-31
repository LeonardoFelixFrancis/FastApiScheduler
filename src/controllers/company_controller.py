from fastapi import Depends, APIRouter
from dependencies import get_company_service
from src.schemas.company_schema import CompanyFilter
from src.interfaces.company.company_service_interface import ICompanyService

router = APIRouter(prefix='/api/company', tags=['companies'])

@router.get('/')
def get_company(id: int | None, name: str | None, company_service: ICompanyService = Depends(get_company_service)):
    return company_service.get(CompanyFilter(id = id, name = name))