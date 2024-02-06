from fastapi import APIRouter, Request, Depends
from app.resource.depends.depends import injection
from injector import inject
from app.resource.service.auth_service import AuthService
from app.resource.request.sign_up_request import (EmailExistsRequest, IdAccountExistsRequest,
    SignUpRequest)
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
    email = request.email
    service = get_di_service(AuthService)
    result = await service.email_exist(email)
    return result

@router.post('/id-account-exists', tags=["auth"] ,response_model=bool)
async def id_account_exists(request: IdAccountExistsRequest) -> bool:
    id_account = request.id_account
    service = get_di_service(AuthService)
    result = await service.id_account_exist(id_account)
    return result