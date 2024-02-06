from app.resource.response.json_response import JsonResponse
from pydantic import BaseModel, Field


class EmailExistsResponse(JsonResponse):
    class EmailExistsResponseItem(BaseModel):
        exists: bool = Field(None, description="存在確認結果")
    data: EmailExistsResponseItem = Field(None, description="存在確認結果")
    
class IdAccountExistsResponse(JsonResponse):
    class IdAccountExistsResponseItem(BaseModel):
        exists: bool = Field(None, description="存在確認結果")
    data: IdAccountExistsResponseItem = Field(None, description="存在確認結果")