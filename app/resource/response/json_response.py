from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Any, Optional

app = FastAPI()

class JsonResponse(BaseModel):
    status: int = Field(200, description="ステータスコード")
    data: Any = Field(None, description="データ")
    message: Optional[str] = Field("ok", description="メッセージ")
