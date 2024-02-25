from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
import logging
from logging.config import dictConfig
from app.config.logging_config import LOGGING_CONFIG
import traceback
from dotenv import load_dotenv
import os
from app.resource.response.error_response import ErrorJsonResponse
from app.app import app

load_dotenv()
# 環境設定を取得
app_env = os.getenv("APP_ENV", "development")

dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("app.exception")
# カスタムエラーハンドラの追加
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    error = ErrorJsonResponse(status=exc.status_code, error="http-error", message=exc.detail)
    return JSONResponse(status_code=exc.status_code, content=error.model_dump())

class EnhancedTracebackMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            logger.error(f"Unhandled exception: {exc}")
            tb_lines = traceback.format_exception(etype=type(exc), value=exc, tb=exc.__traceback__)
            detailed_tb = "".join(tb_lines[::-1])  # スタックトレースを逆順に

            # 本番環境ではスタックトレースをレスポンスに含めない
            if app_env == "production":
                error_detail = "An unexpected error has occurred. Please try again later."
            else:
                error_detail = detailed_tb

            logger.error(f"Reversed traceback: {detailed_tb}")
            logger.error(f"Request path: {request.url.path}, Method: {request.method}")

            error = ErrorJsonResponse(status=500, error='An internal server error occurred', message=error_detail)
            return JSONResponse(status_code=500, content=error.model_dump())

