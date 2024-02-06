from fastapi import FastAPI
import app.resource.controller.auth_controller as auth_controller
from dotenv import load_dotenv
from app.resource.exception.handler import EnhancedTracebackMiddleware


load_dotenv()

app = FastAPI()

app.add_middleware(EnhancedTracebackMiddleware)
app.include_router(auth_controller.router)


