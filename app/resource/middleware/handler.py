import logging
import os
import traceback
from logging.config import dictConfig

from dotenv import load_dotenv
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.app import app
from app.config.logging_config import LOGGING_CONFIG
from app.resource.response.error_response import ErrorJsonResponse
from app.resource.util.lang import convert_lang

load_dotenv()
# 環境設定を取得
app_env = os.getenv("APP_ENV", "development")

dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("app.exception")


# カスタムエラーハンドラの追加
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    error = ErrorJsonResponse(
        detail=[
            {
                "loc": [f"{request.method} {request.url.path}"],
                "msg": exc.detail,
                "type": "http_error",
            }
        ]
    )
    return JSONResponse(status_code=exc.status_code, content=error.model_dump())


class EnhancedTracebackMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            logger.error(f"Unhandled exception: {exc}")
            tb_lines = traceback.format_exception(type(exc), exc, exc.__traceback__)
            detailed_tb = "".join(tb_lines[::-1])  # スタックトレースを逆順に

            # 本番環境ではスタックトレースをレスポンスに含めない
            if app_env == "production":
                error_detail = convert_lang("common_error.internal_server_error")
            else:
                error_detail = detailed_tb

            logger.error(f"Reversed traceback: {detailed_tb}")
            logger.error(f"Request path: {request.url.path}, Method: {request.method}")

            error = ErrorJsonResponse(
                detail=[
                    {
                        "loc": [f"{request.method} {request.url.path}"],
                        "msg": error_detail,
                        "type": "server_error",
                    }
                ]
            )
            return JSONResponse(status_code=500, content=error.model_dump())
