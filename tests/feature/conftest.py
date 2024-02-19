from app.main import app
from app.resource.controller import *
from dotenv import load_dotenv
from httpx import AsyncClient
import pytest_asyncio
import os

load_dotenv()

BASE_URL = os.getenv("BASE_URL")

@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(app=app, base_url=BASE_URL) as client:
        yield client