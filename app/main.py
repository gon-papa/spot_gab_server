import i18n
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles

from app.resource.controller import user_controller
import app.resource.controller.auth_controller as auth_controller
from app.app import app
from app.resource.middleware.handler import EnhancedTracebackMiddleware
from app.resource.middleware.http import LanguageMiddleware

load_dotenv()
app = app
i18n.load_path.append("app/resource/i18n/")
i18n.set("file_format", "json")
i18n.set("locale", "ja")
i18n.set("fallback", "ja")
i18n.set("skip_locale_root_data", True)

# 静的ファイルマウント
app.mount("/public", StaticFiles(directory="app/public"), name="public")

app.include_router(auth_controller.router)
app.include_router(user_controller.router)

app.add_middleware(EnhancedTracebackMiddleware)
app.add_middleware(LanguageMiddleware)
