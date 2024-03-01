from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Any, Union

class JsonResponse(BaseModel):
    status: int = Field(200, description="ステータスコード")
    data: Any = Field(None, description="データ")
    message: Union[str,None] = Field("ok", description="メッセージ")
