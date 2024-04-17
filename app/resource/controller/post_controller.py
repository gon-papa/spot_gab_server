import logging
from fastapi import APIRouter, Depends

from app.resource.middleware.header import common_header
from app.resource.model.users import Users
from app.resource.request.post_request import PostRequest, get_post_form_data
from app.resource.response.json_response import JsonResponse
from app.resource.service_domain.auth_service_domain import get_current_active_user


router = APIRouter()
logger = logging.getLogger("app.exception")


@router.post(
    "/post",
    response_model=JsonResponse,
    tags=["post"],
    name="投稿",
    description="投稿します。",
    operation_id="post",
    dependencies=[Depends(common_header)],
)
async def store(
    request: PostRequest = Depends(get_post_form_data),
    current_user: Users = Depends(get_current_active_user),
):
    try:
        # image_validation_errors = await CustomValidator().validate_image(files)
        # if image_validation_errors != []:
        #     response = ErrorJsonResponse(status_code=400, detail=image_validation_errors)
        #     return FastApiJsonResponse(status_code=400, content=response.model_dump())
        
        # 保存処理
        return JsonResponse(status_code=201, message="投稿しました。")
        
    except Exception:
        raise
    # return JsonResponse(status_code=201, message="投稿しました。")
