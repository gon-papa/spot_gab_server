from app.main import app
from app.resource.controller import *
from datetime import date
from dotenv import load_dotenv
from httpx import AsyncClient
import pytest_asyncio
import os
from app.resource.depends.depends import get_di_class
from app.resource.model.users import Users
from app.resource.repository.user_repository import UserRepository

load_dotenv()

BASE_URL = os.getenv("BASE_URL")

# クライアント取得
@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(app=app, base_url=BASE_URL) as client:
        yield client
        

# 認証ユーザー取得
@pytest_asyncio.fixture
async def get_auth_user(async_client)-> Users:
    user = Users(
        account_name="auth_user",
        id_account="@auth_user",
        email="auth@test.com",
        hashed_password="$2b$12$VUJv82tezCvUccA35HleFulwc4qYrz7BqFHIdK7yXQK0nEPyl2Cc.", # password
        birth_date=date(2000, 1, 1),
        is_active=True,
        refresh_token="test",
        expires_at=date(2000, 1, 1),
    )
    repository = get_di_class(UserRepository)
    await repository.create_user(user)
    response = await async_client.post("/sign_in", data={
        "username": user.email,
        "password": "password"
    })
    refresh_user = await repository.get_user_by_email(user.email)
    refresh_user.__dict__["token"] = response.json()['data']['user']['token']
    return refresh_user
