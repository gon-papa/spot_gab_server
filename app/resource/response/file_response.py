
from typing import List
from pydantic import BaseModel, Field
from app.resource.response.json_response import JsonResponse


class ImageResponse(JsonResponse):
    class ImageResponseItem(BaseModel):
        uuid: str = Field(None, description="画像UUID")
        name: str = Field(None, description="画像名")
        path: str = Field(None, description="画像URL")
    data: List[ImageResponseItem] = Field(None, description="画像URL")
