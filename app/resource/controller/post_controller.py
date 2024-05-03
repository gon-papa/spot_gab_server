import logging
from fastapi import APIRouter, Depends

from app.resource.depends.depends import get_di_class
from app.resource.middleware.header import common_header
from app.resource.model.users import Users
from app.resource.request.post_request import PostRequest
from app.resource.response.json_response import JsonResponse
from app.resource.service.post_service import PostService
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
    request: PostRequest,
    current_user: Users = Depends(get_current_active_user),
):
    try:
        await get_di_class(PostService).store(
            user=current_user,
            request=request,
        )
    except Exception:
        raise
    return JsonResponse(status_code=201, message="投稿しました。")
