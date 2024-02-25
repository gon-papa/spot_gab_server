import app.resource.controller.auth_controller as auth_controller
from dotenv import load_dotenv
from app.resource.middleware.handler import EnhancedTracebackMiddleware
from app.app import app

load_dotenv()
app = app
app.include_router(auth_controller.router)
app.add_middleware(EnhancedTracebackMiddleware)
