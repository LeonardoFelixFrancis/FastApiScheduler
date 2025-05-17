from fastapi import Depends, APIRouter
from dependencies import get_company_service, authenticate
from src.schemas.company_schema import CompanyFilter
from src.interfaces.company.company_service_interface import ICompanyService
from src.models.user import User

router = APIRouter(prefix='/company', tags=['companies'])

@router.get('/')
def get_company(company_service: ICompanyService = Depends(get_company_service), 
                user: User = Depends(authenticate)):
    return company_service.get(CompanyFilter(id = user.company_id, name = None))