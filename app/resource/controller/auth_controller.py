import os

from dotenv import load_dotenv
from fastapi import APIRouter, BackgroundTasks, Depends, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

from app.resource.depends.depends import get_di_class
from app.resource.middleware.header import common_header
from app.resource.model.users import Users
from app.resource.request.auth_request import (
    EmailExistsRequest,
    IdAccountExistsRequest,
    RefreshTokenRequest,
    ResetPasswordRequest,
    ResetPasswordVerifyRequest,
    SignUpRequest,
)
from app.resource.response.auth_response import (
    EmailExistsResponse,
    IdAccountExistsResponse,
    SignInResponse,
    SignUpResponse,
)
from app.resource.response.error_response import ErrorJsonResponse
from app.resource.response.json_response import JsonResponse
from app.resource.service.auth_service import AuthService
from app.resource.service_domain.auth_service_domain import get_current_active_user

from app.resource.util.logging import Log

router = APIRouter()
load_dotenv()


@router.post(
    "/sign-up",
    tags=["auth"],
    response_model=SignUpResponse,
    name="サインアップ",
    description="サインアップ",
    operation_id="sign_up",
    responses={
        400: {
            "model": ErrorJsonResponse,
            "description": "Email or Account ID already registered",
        },
        500: {
            "model": ErrorJsonResponse,
            "description": "Internal Server Error",
        },
    },
    dependencies=[Depends(common_header)],
)
async def sign_up(request: SignUpRequest, bk: BackgroundTasks) -> SignUpResponse:
    try:
        user = await get_di_class(AuthService).sign_up(request, bk)

    except Exception:
        raise
    return SignUpResponse(status=200, data=SignUpResponse.SignUpResponseItem(user=user), message="ok")


@router.post(
    "/sign-in",
    tags=["auth"],
    response_model=SignInResponse,
    name="サインイン",
    description="サインイン",
    operation_id="sign_in",
    responses={
        403: {
            "model": ErrorJsonResponse,
            "description": "Incorrect email or password",
        },
        500: {
            "model": ErrorJsonResponse,
            "description": "Internal Server Error",
        },
    },
    # openApiで認証が使えなくなるので一旦コメントアウト
    # dependencies=[Depends(common_header)]
)
async def sign_in(request: OAuth2PasswordRequestForm = Depends()) -> SignInResponse:
    try:
        email = request.username
        password = request.password
        tokens = await get_di_class(AuthService).sign_in(email, password)
    except Exception:
        Log().errorLog(Exception)
        raise
    return SignInResponse(access_token=tokens["token"], token_type="bearer", refresh_token=tokens["refresh_token"])


@router.post(
    "/sign-out",
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
        },
    },
    dependencies=[Depends(common_header)],
)
async def sign_out(current_user: Users = Depends(get_current_active_user)) -> JsonResponse:
    try:
        result = await get_di_class(AuthService).sign_out(current_user)
    except Exception:
        Log().errorLog(Exception)
        raise
    return JsonResponse(status=200, data={"result": result}, message="ok")


@router.post(
    "/refresh-token",
    tags=["auth"],
    response_model=SignUpResponse,
    name="トークンリフレッシュ",
    description="トークンリフレッシュ",
    operation_id="refresh_token",
    responses={
        403: {
            "model": ErrorJsonResponse,
            "description": "Forbidden",
        },
        500: {
            "model": ErrorJsonResponse,
            "description": "Internal Server Error",
        },
    },
    dependencies=[Depends(common_header)],
)
async def refresh_token(request: RefreshTokenRequest) -> SignUpResponse:
    try:
        user = await get_di_class(AuthService).get_refresh_token(request.refresh_token)
    except Exception:
        Log().errorLog(Exception)
        raise
    return SignUpResponse(status=200, data=SignUpResponse.SignUpResponseItem(user=user), message="ok")


@router.post(
    "/email-exists",
    tags=["auth"],
    response_model=EmailExistsResponse,
    name="メールアドレスの存在確認",
    description="emailの存在確認。ture: 存在する, false: 存在しない",
    operation_id="email_exists",
    dependencies=[Depends(common_header)],
)
async def email_exists(request: EmailExistsRequest) -> EmailExistsResponse:
    try:
        email = request.email
        service = get_di_class(AuthService)
        result = await service.email_exist(email)

        return EmailExistsResponse(
            status=200, data=EmailExistsResponse.EmailExistsResponseItem(exists=result), message="ok"
        )
    except Exception:
        Log().errorLog(Exception)
        raise


@router.post(
    "/id-account-exists",
    tags=["auth"],
    response_model=IdAccountExistsResponse,
    name="id_accountの存在確認",
    description="id_accountの存在確認。ture: 存在する, false: 存在しない",
    operation_id="id_account_exists",
    dependencies=[Depends(common_header)],
)
async def id_account_exists(request: IdAccountExistsRequest) -> IdAccountExistsResponse:
    id_account = request.id_account
    service = get_di_class(AuthService)
    result = await service.id_account_exist(id_account)
    return IdAccountExistsResponse(
        status=200, data=IdAccountExistsResponse.IdAccountExistsResponseItem(exists=result), message="ok"
    )


@router.get(
    "/verify-email/{token}/{lang}",
    tags=["auth"],
    response_class=HTMLResponse,
    response_model=None,
    name="メールアドレスの確認",
    description="メールアドレスの確認",
    operation_id="verify_email",
)
async def verify_email(request: Request, token: str, lang: str) -> HTMLResponse:
    templates = Jinja2Templates(directory="app/resource/templates")
    try:
        await get_di_class(AuthService).email_verify(token)
        if lang == "en":
            return templates.TemplateResponse(
                request, "verify-email-en.html", {"suppout_url": os.getenv("SUPPORT_URL")}
            )
        return templates.TemplateResponse(request, "verify-email-ja.html", {"suppout_url": os.getenv("SUPPORT_URL")})
    except Exception:
        Log().errorLog(Exception)
        if lang == "en":
            return templates.TemplateResponse(
                request, "faild-verify-en.html", {"suppout_url": os.getenv("SUPPORT_URL")}
            )
        return templates.TemplateResponse(request, "faild-verify-ja.html", {"suppout_url": os.getenv("SUPPORT_URL")})


@router.post(
    "/password-reset",
    tags=["auth"],
    response_model=JsonResponse,
    name="パスワードリセット",
    description="パスワードリセットメールを送信する",
    operation_id="reset_password",
    dependencies=[Depends(common_header)],
)
async def reset_password_send_mail(request: ResetPasswordRequest, bk: BackgroundTasks) -> JsonResponse:
    try:
        await get_di_class(AuthService).reset_password_send_mail(request.email, bk)
        return JsonResponse(status=200, data={"result": "ok"}, message="ok")
    except Exception:
        Log().errorLog(Exception)
        raise


@router.get(
    "/password-reset/{token}/{lang}",
    tags=["auth"],
    response_class=HTMLResponse,
    response_model=None,
    name="パスワードリセット画面",
    description="パスワードリセット画面",
    operation_id="password_reset_page",
)
async def reset_password_page(request: Request, token: str, lang: str) -> HTMLResponse:
    templates = Jinja2Templates(directory="app/resource/templates")
    try:
        await get_di_class(AuthService).reset_password_page_check(token)
        if lang == "en":
            return templates.TemplateResponse(
                request,
                "reset-password-en.html",
                {
                    "token": token,
                    "lang": lang,
                    "suppout_url": os.getenv("SUPPORT_URL"),
                    "base_url": os.getenv("BASE_URL"),
                }
            )
        return templates.TemplateResponse(
            request,
            "reset-password-ja.html",
            {
                "token": token,
                "lang": lang,
                "suppout_url": os.getenv("SUPPORT_URL"),
                "base_url": os.getenv("BASE_URL"),
            }
        )
    except Exception as e:
        Log().errorLog(e)
        if lang == "en":
            return templates.TemplateResponse(
                request, "faild-verify-en.html", {"suppout_url": os.getenv("SUPPORT_URL")}
            )
        return templates.TemplateResponse(request, "faild-verify-ja.html", {"suppout_url": os.getenv("SUPPORT_URL")})


@router.post(
    "/password-reset-verify",
    tags=["auth"],
    response_class=HTMLResponse,
    response_model=None,
    name="パスワードリセット認証",
    description="パスワードリセット認証",
    operation_id="password_reset_verify",
)
async def password_reset_verify(
    request: Request,
    password: str = Form(...),
) -> HTMLResponse:
    templates = Jinja2Templates(directory="app/resource/templates")
    try:
        # ミドルウェアでパスパラメータは処理できないので、クエリパラメータで代用
        token = request.query_params.get("token")
        lang = request.query_params.get("language")
        ResetPasswordVerifyRequest(
            password=password,
        )
        await get_di_class(AuthService).password_reset_verify(token, password)
        if lang == "en":
            return templates.TemplateResponse(
                request, "success-reset-password-ja.html", {"suppout_url": os.getenv("SUPPORT_URL")}
            )
        return templates.TemplateResponse(
            request, "success-reset-password-ja.html", {"suppout_url": os.getenv("SUPPORT_URL")}
        )
    except ValidationError as e:
        errors_list = []
        for error in e.errors():
            error_copy = error.copy()
            error_copy["msg"] = error_copy["msg"].replace("Value error, ", "")
            errors_list.append(error_copy)

        if lang == "en":
            return templates.TemplateResponse(
                request,
                "reset-password-en.html",
                {
                    "token": token,
                    "lang": lang,
                    "suppout_url": os.getenv("SUPPORT_URL"),
                    "base_url": os.getenv("BASE_URL"),
                    "errors": errors_list
                }
            )
        return templates.TemplateResponse(
            request,
            "reset-password-ja.html",
            {
                "token": token,
                "lang": lang,
                "suppout_url": os.getenv("SUPPORT_URL"),
                "base_url": os.getenv("BASE_URL"),
                "errors": errors_list
            }
        )
    except Exception as e:
        Log().errorLog(e)
        if lang == "en":
            return templates.TemplateResponse(
                request, "faild-verify-en.html", {"suppout_url": os.getenv("SUPPORT_URL")}
            )
        return templates.TemplateResponse(request, "faild-verify-ja.html", {"suppout_url": os.getenv("SUPPORT_URL")})
