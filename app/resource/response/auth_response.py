from pydantic import BaseModel, Field

from app.resource.model.users import AuthenticatedUser
from app.resource.response.json_response import JsonResponse


class EmailExistsResponse(JsonResponse):
    class EmailExistsResponseItem(BaseModel):
        exists: bool = Field(None, description="存在確認結果")

    data: EmailExistsResponseItem = Field(None, description="存在確認結果")


class IdAccountExistsResponse(JsonResponse):
    class IdAccountExistsResponseItem(BaseModel):
        exists: bool = Field(None, description="存在確認結果")

    data: IdAccountExistsResponseItem = Field(None, description="存在確認結果")


class SignUpResponse(JsonResponse):
    class SignUpResponseItem(BaseModel):
        user: AuthenticatedUser = Field(None, description="サインアップユーザー情報")

    data: SignUpResponseItem = Field(None, description="サインアップユーザー情報")


class SignInResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: str
