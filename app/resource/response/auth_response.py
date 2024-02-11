from app.resource.response.json_response import JsonResponse
from pydantic import BaseModel, Field
from app.resource.model.users import Users


class EmailExistsResponse(JsonResponse):
    class EmailExistsResponseItem(BaseModel):
        exists: bool = Field(None, description="存在確認結果")
    data: EmailExistsResponseItem = Field(None, description="存在確認結果")
    
class IdAccountExistsResponse(JsonResponse):
    class IdAccountExistsResponseItem(BaseModel):
        exists: bool = Field(None, description="存在確認結果")
    data: IdAccountExistsResponseItem = Field(None, description="存在確認結果")
    
class LoginResponse(JsonResponse):
    class LoginResponseItem(BaseModel):
        user: Users = Field(None, description="ログインユーザー情報")
    data: LoginResponseItem = Field(None, description="ログイン情報")