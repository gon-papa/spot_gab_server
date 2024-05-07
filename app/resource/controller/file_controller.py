

from typing import List
from fastapi import APIRouter, Depends, UploadFile, File

from app.resource.depends.depends import get_di_class
from app.resource.middleware.header import common_header
from app.resource.model.users import Users
from app.resource.request.common_validate import CustomValidator
from app.resource.response.error_response import ErrorJsonResponse
from app.resource.response.file_response import ImageResponse
from fastapi.responses import JSONResponse as FastApiJsonResponse

from app.resource.service.file_service import FileService
from app.resource.service_domain.auth_service_domain import get_current_active_user
from app.resource.util.logging import Log

router = APIRouter()


@router.post(
    "/image/upload",
    response_model=ImageResponse,
    tags=["file"],
    name="ファイルアップロード",
    description="ファイルアップロードします。",
    operation_id="image_upload",
    dependencies=[Depends(common_header)],
)
async def image_upload(
    images: List[UploadFile] = File(...),
    current_user: Users = Depends(get_current_active_user),
):
    try:
        image_validation_errors = await CustomValidator().validate_image(images=images)
        if image_validation_errors != []:
            response = ErrorJsonResponse(status_code=400, detail=image_validation_errors)
            return FastApiJsonResponse(status_code=400, content=response.model_dump())
        # 保存処理
        saved_images = await get_di_class(FileService).create(
            files=images,
            user_uuid=current_user.uuid,
        )
        saved_image_items = []
        for saved_image in saved_images:
            saved_image_items.append(
                ImageResponse.ImageResponseItem(
                    uuid=saved_image.uuid,
                    name=saved_image.name,
                    path=saved_image.path,
                )
            )
    except Exception:
        Log().errorLog(Exception)
        raise
    return ImageResponse(
        status=200,
        data=saved_image_items,
    )

# deleteも作成
