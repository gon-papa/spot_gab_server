from fastapi import APIRouter, Request, Depends
from app.resource.depends.depends import injection
from injector import inject
from app.resource.service.auth_service import AuthService
from app.resource.request.sign_up_request import SignUpRequest, EmailExistsRequest
import injector

router = APIRouter()

@inject
def get_di_service(_class):
    return injection.get(_class)

# @router.post('/sign_up', tags=["auth"] ,response_model=dict)
# async def sign_up(request: SignUpRequest) -> dict:
#     return get_di_service(AuthService).sign_up()

@router.post('/email-exists', tags=["auth"] ,response_model=bool)
async def email_exists(request: EmailExistsRequest) -> bool:
    mail = request.email
    service = get_di_service(AuthService)
    result = await service.email_exist(mail)
    return result

# @router.post('/account-id-exists', tags=["auth"] ,response_model=dict)
# async def account_id_exists(request: Request) -> dict:
#     return get_di_service(AuthService).account_id_exists()