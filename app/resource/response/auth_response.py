from app.resource.response.json_response import JsonResponse
from pydantic import BaseModel, Field
from app.resource.model.users import SignInUser, UserRead


class EmailExistsResponse(JsonResponse):
    class EmailExistsResponseItem(BaseModel):
        exists: bool = Field(None, description="存在確認結果")
    data: EmailExistsResponseItem = Field(None, description="存在確認結果")
    
class IdAccountExistsResponse(JsonResponse):
    class IdAccountExistsResponseItem(BaseModel):
        exists: bool = Field(None, description="存在確認結果")
    data: IdAccountExistsResponseItem = Field(None, description="存在確認結果")
    
class SignInResponse(JsonResponse):
    class SignInResponseItem(BaseModel):
        user: SignInUser = Field(None, description="サインインユーザー情報")
    data: SignInResponseItem = Field(None, description="サインインユーザー情報")