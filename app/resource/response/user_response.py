from pydantic import BaseModel, Field

from app.resource.model.users import Me
from app.resource.response.json_response import JsonResponse


class MeResponse(JsonResponse):
    class MeResponseItem(BaseModel):
        user: Me = Field(None, description="ユーザー情報")
    data: MeResponseItem = Field(None, description="ユーザー情報")