import i18n
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles

from app.resource.controller import auth_controller, file_controller, post_controller, user_controller
from app.app import app
from app.resource.middleware.handler import EnhancedTracebackMiddleware
from app.resource.middleware.http import LanguageMiddleware

load_dotenv()
app = app

# locale
i18n.load_path.append("app/resource/i18n/")
i18n.set("file_format", "json")
i18n.set("locale", "ja")
i18n.set("fallback", "ja")
i18n.set("skip_locale_root_data", True)

# 静的ファイルマウント
app.mount("/public", StaticFiles(directory="app/public"), name="public")

# routes
app.include_router(auth_controller.router)
app.include_router(user_controller.router)
app.include_router(post_controller.router)
app.include_router(file_controller.router)

# ミドルウェア
app.add_middleware(EnhancedTracebackMiddleware)
app.add_middleware(LanguageMiddleware)
