from datetime import date
from dotenv import load_dotenv
import logging
import os
import pytest
import asyncio
from app.resource.repository.user_repository import UserRepository
from app.resource.model.users import Users
from app.app import app
from httpx import AsyncClient

load_dotenv()

client = AsyncClient(app=app, base_url=os.getenv("BASE_URL"))

@pytest.mark.asyncio
async def test_email_exists_メールアドレスが存在したらtrueを返す(set_up_test):
    user = Users(
        account_name = "test",
        id_account = "test",
        email = "test@test.com",
        hashed_password = "test",
        birth_date = date(2000, 1, 1),
        is_active = True,
        refresh_token = "test",
        expires_at = date(2000, 1, 1)
    )
    repository = UserRepository()
    await repository.create_user(user)

    response = await client.post('/email-exists', json={"email": "test@test.com"})
    assert response.status_code == 200
    assert response.json() == {"exists": True}
    
    