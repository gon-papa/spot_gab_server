import logging
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, WebSocketException

from app.resource.depends.depends import get_di_class
from app.resource.middleware.header import common_header
from app.resource.model.users import Users
from app.resource.request.user_location_request import UserLocationRequest
from app.resource.response.error_response import ErrorJsonResponse
from app.resource.response.json_response import JsonResponse
from app.resource.service.user_location_service import UserLocationSercice
from app.resource.service_domain.auth_service_domain import get_current_active_user
from app.resource.service_domain.user_location_manager_service_domain import UserLocationManager


router = APIRouter()
logger = logging.getLogger("app.exception")
manager = UserLocationManager()

@router.post(
    "/user-location",
    tags=["user_location"],
    response_model=JsonResponse,
    name="ユーザーの位置情報を保存する",
    description="ユーザーの位置情報を保存します。",
    operation_id="post_user_location",
    responses={
        401: {
            "model": ErrorJsonResponse,
            "description": "Unauthorized",
        },
        500: {
            "model": ErrorJsonResponse,
            "description": "Internal Server Error",
        },
    },
    dependencies=[Depends(common_header)],
)
async def user_location(
    request: UserLocationRequest,
    current_user: Users = Depends(get_current_active_user)
) -> JsonResponse:
    try:
        await get_di_class(UserLocationSercice).save_location(request, current_user)
    except Exception:
        raise
    return JsonResponse(
        status=200,
        message="ok",
    )


@router.websocket(
    "ws/user-location",
    tags=["user_location"],
    name="ユーザーの位置情報をリアルタイムで共有する",
    description="ユーザーの位置情報をリアルタイムで共有するためのWebSocket接続を行います",
    operation_id="get_user_location",
    responses={
        401: {
            "model": ErrorJsonResponse,
            "description": "Unauthorized",
        },
        500: {
            "model": ErrorJsonResponse,
            "description": "Internal Server Error",
        },
    },
)
async def user_location_websocket(
    websocket: WebSocket,
    current_user: Users = Depends(get_current_active_user)
):
    try:
        await get_di_class(UserLocationManager).connect(current_user.uuid)
        # 常に画面の中心の緯度経度を送信してもらう必要があるかもしれない。そこから近くのユーザーのみに送信するようにする。
    except WebSocketDisconnect:
        raise
    except WebSocketException:
        raise
    except Exception:
        get_di_class(UserLocationManager).disconnect(current_user.uuid)
    return JsonResponse(
        status=200,
        message="ok",
    )
