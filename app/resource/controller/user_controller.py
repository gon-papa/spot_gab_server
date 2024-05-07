from fastapi import APIRouter, Depends

from app.resource.depends.depends import get_di_class
from app.resource.middleware.header import common_header
from app.resource.model.users import Users
from app.resource.request.user_request import UserProfileRequest
from app.resource.response.error_response import ErrorJsonResponse
from app.resource.response.json_response import JsonResponse
from app.resource.response.user_response import MeResponse
from app.resource.service.user_service import UserService
from app.resource.service_domain.auth_service_domain import get_current_active_user
from app.resource.util.logging import Log

router = APIRouter()


@router.get(
    "/me",
    response_model=MeResponse,
    tags=["user"],
    name="マイページ用ユーザー取得(自身と他人含む)",
    description="マイページ用ユーザー取得(自身と他人含む)",
    operation_id="get_me",
    dependencies=[Depends(common_header)],
)
async def me(current_user: Users = Depends(get_current_active_user)):
    try:
        # TODO フォロー、フォロワー数も入れ込む
        current_user
    except Exception:
        Log().errorLog(Exception)
        raise
    return MeResponse(status=200, data=MeResponse.MeResponseItem(user=current_user))


@router.post(
    "/user/profile",
    response_model=JsonResponse,
    tags=["user"],
    name="ユーザープロフィール保存",
    description="ユーザープロフィールを保存します。",
    operation_id="save_user_profile",
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
async def save_user_profile(request: UserProfileRequest, current_user: Users = Depends(get_current_active_user)):
    try:
        await get_di_class(UserService).save_profile(current_user, request)
    except Exception:
        Log().errorLog(Exception)
        raise
    return JsonResponse(status=200, message="ok")
