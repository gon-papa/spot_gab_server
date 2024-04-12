from pydantic import BaseModel, Field

from app.resource.model.users import AuthenticatedUser
from app.resource.response.json_response import JsonResponse


class UserResponse(JsonResponse):
    class UserResponseItem(BaseModel):
        user: AuthenticatedUser = Field(None, description="ユーザー情報")
    data: UserResponseItem = Field(None, description="ユーザー情報")