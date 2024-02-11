import app.resource.controller.auth_controller as auth_controller
from dotenv import load_dotenv
from app.resource.exception.handler import EnhancedTracebackMiddleware
from app.app import app


load_dotenv()

app.add_middleware(EnhancedTracebackMiddleware)
app.include_router(auth_controller.router)
