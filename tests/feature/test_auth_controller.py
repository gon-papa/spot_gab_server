from datetime import date
import pytest
from app.resource.repository.user_repository import UserRepository
from app.resource.model.users import Users

# テストコマンド
# pytest tests/feature/test_auth_controller.py

class TestAuthController:
    @pytest.mark.asyncio
    async def test_email_exists_メールアドレスが存在したらtrueを返す(self, async_client):
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
        
        response = await async_client.post('/email-exists', json={"email": "test@test.com"})
        print(response.text)
        assert response.status_code == 200
        assert response.json()['data'] == {"exists": True}

    @pytest.mark.asyncio
    async def test_email_exists_メールアドレスが存在しなければfalseを返す(self, async_client):    
        response = await async_client.post('/email-exists', json={"email": "test@test.com"})
        print(response.text)
        assert response.status_code == 200
        assert response.json()['data'] == {"exists": False}
    
    