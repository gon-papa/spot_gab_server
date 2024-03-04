from dotenv import load_dotenv
from fastapi import APIRouter, BackgroundTasks, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from app.resource.depends.depends import get_di_class
from app.resource.middleware.header import common_header
from app.resource.service.auth_service import AuthService
from app.resource.request.auth_request import (
    SignUpRequest,
    EmailExistsRequest,
    IdAccountExistsRequest,
    RefreshTokenRequest
)
from app.resource.response.auth_response import (
    EmailExistsResponse,
    IdAccountExistsResponse,
    SignUpResponse,
    SignInResponse
)
from app.resource.response.error_response import ErrorJsonResponse
from app.resource.response.json_response import JsonResponse
from app.resource.model.users import Users
from app.resource.service_domain.auth_service_domain import get_current_active_user
import os

router = APIRouter()
load_dotenv()

@router.post(
    '/sign-up',
    tags=["auth"],
    response_model=SignUpResponse,
    name="サインアップ",
    description="サインアップ",
    operation_id="sign_up",
    responses = {
        400: {
            "model": ErrorJsonResponse,
            "description": "Email or Account ID already registered",
        },
        500: {
            "model": ErrorJsonResponse,
            "description": "Internal Server Error",
        }
    },
    dependencies=[Depends(common_header)]
)
async def sign_up(request: SignUpRequest, bk: BackgroundTasks) -> SignUpResponse:
    try:
        user = await get_di_class(AuthService).sign_up(request, bk)
    except Exception as e:
        raise e
    return SignUpResponse(status=200, data={"user": user})
        

@router.post(
    '/sign-in',
    tags=["auth"],
    response_model=SignInResponse,
    name="サインイン",
    description="サインイン",
    operation_id="sign_in",
    responses = {
        401: {
            "model": ErrorJsonResponse,
            "description": "Unauthorized",
        },
        500: {
            "model": ErrorJsonResponse,
            "description": "Internal Server Error",
        }
    },
    dependencies=[Depends(common_header)]
)
async def sign_in(request: OAuth2PasswordRequestForm = Depends()) -> SignInResponse:
    try:
        email = request.username
        password = request.password
        token = await get_di_class(AuthService).sign_in(email, password)
    except Exception as e:
        raise e
    return SignInResponse(access_token=token, token_type="bearer")

@router.post(
    '/sign-out',
    tags=["auth"],
    response_model=JsonResponse,
    name="サインアウト",
    description="サインアウト",
    operation_id="sign_out",
    responses={
        400: {
            "model": ErrorJsonResponse,
            "description": "Inactive user",
        },
        401: {
            "model": ErrorJsonResponse,
            "description": "Not authenticated",
        }
    },
    dependencies=[Depends(common_header)]
)
async def sign_out(current_user: Users = Depends(get_current_active_user)) -> JsonResponse:
    try:
        result = await get_di_class(AuthService).sign_out(current_user)
    except Exception as e:
        raise e
    return JsonResponse(status=200, data={"result": result})

@router.post(
    '/refresh-token',
    tags=["auth"],
    response_model=SignUpResponse,
    name="トークンリフレッシュ",
    description="トークンリフレッシュ",
    operation_id="refresh_token",
    responses={
        401: {
            "model": ErrorJsonResponse,
            "description": "Unauthorized",
        },
        500: {
            "model": ErrorJsonResponse,
            "description": "Internal Server Error",
        }
    },
    dependencies=[Depends(common_header)]
)
async def refresh_token(request: RefreshTokenRequest) -> SignUpResponse:
    try:
        user = await get_di_class(AuthService).get_refresh_token(request.refresh_token)
    except Exception as e:
        raise e
    return SignUpResponse(status=200, data={"user": user})

@router.post(
    '/email-exists',
    tags=["auth"],
    response_model=EmailExistsResponse,
    name="メールアドレスの存在確認",
    description="emailの存在確認。ture: 存在する, false: 存在しない",
    operation_id="email_exists",
    dependencies=[Depends(common_header)]
)
async def email_exists(request: EmailExistsRequest) -> EmailExistsResponse:
    try:
        email = request.email
        service = get_di_class(AuthService)
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
    operation_id="id_account_exists",
    dependencies=[Depends(common_header)]
)
async def id_account_exists(request: IdAccountExistsRequest) -> IdAccountExistsResponse:
    id_account = request.id_account
    service = get_di_class(AuthService)
    result = await service.id_account_exist(id_account)
    return IdAccountExistsResponse(status=200, data={"exists": result})

@router.get(
    '/verify-email/{token}',
    tags=["auth"],
    response_class=HTMLResponse,
    response_model=None,
    name="メールアドレスの確認",
    description="メールアドレスの確認",
    operation_id="verify_email",
)
async def verify_email(request: Request, token: str) -> HTMLResponse:
    templates = Jinja2Templates(directory="app/resource/templates")
    try:
        await get_di_class(AuthService).email_verify(token)
        return templates.TemplateResponse(
            request,
            "verify-email.html",
            {
                "suppout_url": os.getenv('SUPPORT_URL')
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            request,
            "faild-verify-email.html",
            {
                "suppout_url": os.getenv('SUPPORT_URL')
            }
        )

# #メール再設定
# @router.post(
#     '/reset-email/',
#     tags=["auth"],
#     response_class=HTMLResponse,
#     response_model=None,
#     name="メール再設定送信",
#     description="メール再設定送信",
#     operation_id="reset_email"
# )
# async def reset_email(request: Request, current_user: Users = Depends(get_current_active_user)) -> HTMLResponse:
    
    