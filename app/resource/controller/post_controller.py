import logging
from fastapi import APIRouter, Depends

from app.resource.depends.depends import get_di_class
from app.resource.middleware.header import common_header
from app.resource.model.users import Users
from app.resource.request.post_request import PostIndexRequest, PostRequest
from app.resource.response.json_response import JsonResponse
from app.resource.response.post_response import PostResponse
from app.resource.service.post_service import PostService
from app.resource.service_domain.auth_service_domain import get_current_active_user


router = APIRouter()
logger = logging.getLogger("app.exception")


@router.get(
    "/post",
    response_model=JsonResponse,
    tags=["post"],
    name="投稿一覧",
    description="投稿一覧を取得します。",
    operation_id="getPostList",
    dependencies=[Depends(common_header)],
)
async def index(
    params: PostIndexRequest = Depends(),
    current_user: Users = Depends(get_current_active_user),
):
    try:
        results = await get_di_class(PostService).index(
            user=current_user,
            request=params,
        )
        responseArray = []
        for result in results:
            print('PPAP')
            print(result.images)
            result.images
            responseArray.append(
                PostResponse.PostResponseItem(
                    post=result,
                    postImages=result.images,
                    user=result.user,
                    location=result.location,
                )
            )
        return JsonResponse(status_code=200, message="投稿一覧を取得しました。", data=responseArray)
    except Exception:
        raise


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
