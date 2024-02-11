from fastapi import FastAPI, APIRouter, HTTPException
from app.resource.depends.depends import injection
from injector import inject
from app.resource.service.auth_service import AuthService
from app.resource.request.auth_request import (
    EmailExistsRequest,
    IdAccountExistsRequest,
    SignInRequest
)
import injector
from fastapi.security import OAuth2PasswordBearer
from app.resource.exception.handler import logger
from app.resource.response.json_response import JsonResponse
from app.resource.response.auth_response import (EmailExistsResponse, IdAccountExistsResponse,
    SignInResponse)
from app.app import app
from app.resource.response.error_response import ErrorJsonResponse
from app.resource.model.users import UserRead

router = APIRouter()

@inject
def get_di_service(_class):
    return injection.get(_class)

# @router.post('/sign_up', tags=["auth"] ,response_model=dict)
# async def sign_up(request: SignUpRequest) -> dict:
#     return get_di_service(AuthService).sign_up()

@router.post(
    '/sign_in',
    tags=["auth"],
    response_model=SignInResponse,
    name="サインイン",
    description="サインイン",
    operation_id="sign_in",
    responses = {
        403: {
            "model": ErrorJsonResponse,
            "description": "Forbidden - Invalid email or password",
        },
        500: {
            "model": ErrorJsonResponse,
            "description": "Internal Server Error",
        }
    }
)
async def sign_in(request: SignInRequest) -> SignInResponse:
    try:
        email = request.email
        password = request.password
        user = await get_di_service(AuthService).sign_in(email, password)
        if user is None:
            raise HTTPException(status_code=403, detail="Invalid email or password")
    except Exception as e:
        raise e
    return SignInResponse(status=200, data={"user": UserRead.model_validate(user)})

@router.post(
    '/email-exists',
    tags=["auth"],
    response_model=EmailExistsResponse,
    name="メールアドレスの存在確認",
    description="emailの存在確認。ture: 存在する, false: 存在しない",
    operation_id="email_exists"   
)
async def email_exists(request: EmailExistsRequest) -> EmailExistsResponse:
    try:
        email = request.email
        service = get_di_service(AuthService)
        result = await service.email_exist(email)
        return EmailExistsResponse(status=200, data={"exists": result})
    except Exception as e:
        raise e

@router.post(
    '/id-account-exists',
    tags=["auth"],
    response_model=IdAccountExistsResponse,
    name="id_accountの存在確認",
    description="id_accountの存在確認。ture: 存在する, false: 存在しない",
    operation_id="id_account_exists"
)
async def id_account_exists(request: IdAccountExistsRequest) -> IdAccountExistsResponse:
    id_account = request.id_account
    service = get_di_service(AuthService)
    result = await service.id_account_exist(id_account)
    return IdAccountExistsResponse(status=200, data={"exists": result})