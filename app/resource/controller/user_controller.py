from fastapi import APIRouter, Depends, File, Form, UploadFile
import logging
from pathlib import Path

from fastapi.responses import JSONResponse as FastApiJsonResponse

from app.resource.depends.depends import get_di_class
from app.resource.middleware.header import common_header
from app.resource.model.users import Users
from app.resource.request.user_request import UserProfileRequest
from app.resource.response.error_response import ErrorJsonResponse
from app.resource.response.json_response import JsonResponse
from app.resource.response.user_response import UserResponse
from app.resource.service.user_service import UserService
from app.resource.service_domain.auth_service_domain import get_current_active_user

router = APIRouter()
logger = logging.getLogger("app.exception")


@router.get(
    "/me",
    response_model=UserResponse,
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
        raise
    return UserResponse(status=200, data=UserResponse.UserResponseItem(user=current_user))


@router.post(
    "/user/profile",
    response_model=JsonResponse,
    tags=["user"],
    name="ユーザープロフィール保存",
    description="ユーザープロフィールを保存します。",
    operation_id="save_user_profile",
    dependencies=[Depends(common_header)],
)
async def save_user_profile(
    accountName: str = Form(None),
    link: str = Form(None),
    profile: str = Form(None),
    image: UploadFile = File(None),
    current_user: Users = Depends(get_current_active_user),
):
    try:
        current = Path()
        print(current)
        # 手動バリデーション
        validation_errors = await UserProfileRequest().validation(accountName, link, profile, image)
        if validation_errors is not None:
            response = ErrorJsonResponse(status_code=400, detail=validation_errors)
            return FastApiJsonResponse(status_code=400, content=response.model_dump())
        # 保存処理
        await get_di_class(UserService).save_profile(current_user, accountName, link, profile, image)
    except Exception:
        raise
    return JsonResponse(status_code=204, message="ok")
