import contextvars

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()

# コンテキスト変数の定義
current_language = contextvars.ContextVar("current_language", default="en")


class LanguageMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # ヘッダーから言語設定を取得し、コンテキスト変数にセット
        language = request.headers.get("x-language")
        if not language:
            language = request.query_params.get("language", "en")
        token = current_language.set(language)
        response = await call_next(request)
        current_language.reset(token)
        return response
