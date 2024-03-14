from typing import Any, Union
from pydantic import BaseModel, Field


class JsonResponse(BaseModel):
    status: int = Field(200, description="ステータスコード")
    data: Any = Field(None, description="データ")
    message: Union[str, None] = Field("ok", description="メッセージ")
