from pydantic import BaseModel, Field

class ErrorJsonResponse(BaseModel):
    status: int = Field(500, description="ステータスコード")
    error: str = Field("Internal Server Error", description="エラーメッセージ")
    message: str = Field("Internal Server Error", description="エラーメッセージ")