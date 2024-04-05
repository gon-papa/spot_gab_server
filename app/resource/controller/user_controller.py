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
from app.resource.service.user_service import UserService
from app.resource.service_domain.auth_service_domain import get_current_active_user

router = APIRouter()
logger = logging.getLogger("app.exception")


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
    profile: str = Form(...), image: UploadFile = File(None), current_user: Users = Depends(get_current_active_user)
):
    try:
        current = Path()
        print(current)
        # 手動バリデーション
        validation_errors = await UserProfileRequest().validation(profile, image)
        if validation_errors is not None:
            response = ErrorJsonResponse(status_code=400, detail=validation_errors)
            return FastApiJsonResponse(status_code=400, content=response.model_dump())
        # 保存処理
        await get_di_class(UserService).save_profile(current_user, profile, image)
    except Exception:
        raise
    return JsonResponse(status_code=204, message="ok")
