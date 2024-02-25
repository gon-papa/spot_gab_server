from dotenv import load_dotenv
import os
from fastapi import Header, HTTPException
from pydantic import BaseModel, Field

load_dotenv()

class CommonHeader(BaseModel):
    user_agent: str = Field(
        ...,
        title="アカウント名",
        description="アカウント名",
    )
    x_language: str

def common_header(
    x_language: str = Header(
        ...,
        alias="X-Language",
        description="言語[ja,en]",
        openapi_examples={
            "ja": {
                "summary": "Japanese",
                "value": "ja"
            },
            "en": {
                "summary": "English",
                "value": "en"
            }
        }
    ),
    x_user_agent: str = Header(
        ...,
        alias="X-User-Agent",
        description="カスタムUser-Agent",
        openapi_examples={
            "spot-gab-app": {
                "summary": "アプリからのリクエスト",
                "value": "spot-gab-app"
            }
        }
    ),
) -> None:
    if x_language not in os.getenv('LOCALE').split(","):
        x_language = "en"
    print(x_user_agent)
    if x_user_agent != os.getenv('USER_AGENT'):
        raise HTTPException(status_code=400, detail="User-Agent is invalid")