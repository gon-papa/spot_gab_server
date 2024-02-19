from datetime import date
import pytest
import pytest_asyncio
from app.resource.repository.user_repository import UserRepository
from app.resource.model.users import Users
from app.resource.depends.depends import get_di_class

# テストコマンド
# pytest tests/feature/test_auth_controller.py

class TestAuthController:
    @pytest_asyncio.fixture
    async def setup_user(self):
        self.user = Users(
            account_name="test",
            id_account="test",
            email="test@test.com",
            hashed_password="$2b$12$VUJv82tezCvUccA35HleFulwc4qYrz7BqFHIdK7yXQK0nEPyl2Cc.", # password
            birth_date=date(2000, 1, 1),
            is_active=True,
            refresh_token="test",
            expires_at=date(2000, 1, 1)
        )
        repository = get_di_class(UserRepository)
        await repository.create_user(self.user)

    @pytest.mark.asyncio
    async def test_sign_up_サインアップが成功する(self, async_client):
        response = await async_client.post('/sign_up', json={
            "account_name": "test_name",
            "id_account": "test_account_id",
            "email": "signup@test.com",
            "password": "Password",
            "birth_date": "2024-02-19"
        })
        repository = get_di_class(UserRepository)
        user = await repository.get_user_by_email("signup@test.com")
        actual = response.json()

        assert user.is_active == True
        assert response.status_code == 200
        assert actual['data']['user']['token'] is not None
        actual["data"]["user"].pop("token")# tokenは存在確認で十分なので削除
        assert actual == {
            "status": 200,
            "data": {
                "user": {
                    "id": user.id,
                    "uuid": user.uuid,
                    "account_name": user.account_name,
                    "id_account": user.id_account,
                    "email": user.email,
                    "birth_date": user.birth_date.strftime("%Y-%m-%d"),
                    "other_user_invitation_code": user.other_user_invitation_code,
                    "refresh_token": user.refresh_token,
                    "expires_at": user.expires_at.isoformat(),
                    "deleted_at": None,
                    "created_at": user.created_at.isoformat(),
                    "updated_at": user.updated_at.isoformat(),
                },
            },
            "message": "ok"
        }
    
    @pytest.mark.asyncio
    async def test_sign_up_メールアドレスが登録済みなら400エラーを返す(self, async_client, setup_user):
        response = await async_client.post('/sign_up', json={
            "account_name": "test_name",
            "id_account": "test_account_id",
            "email": "test@test.com",
            "password": "Password",
            "birth_date": "2024-02-19"
        })
        assert response.status_code == 400
        assert response.json() == {
            "error": "http-error",
            "status": 400,
            "message": "Email already registered",
        }
        
    @pytest.mark.asyncio
    async def test_sign_up_アカウントIDが登録済みなら400エラーを返す(self, async_client, setup_user):
        response = await async_client.post('/sign_up', json={
            "account_name": "test_name",
            "id_account": "test",
            "email": "signup@test.com",
            "password": "Password",
            "birth_date": "2024-02-19"
        })
        assert response.status_code == 400
        assert response.json() == {
            "error": "http-error",
            "status": 400,
            "message": "Account ID already registered",
        }
        
    @pytest.mark.asyncio
    async def test_sign_in_サインインが成功する(self, async_client, setup_user):
        response = await async_client.post('/sign_in', data={
            "username": "test@test.com",
            "password": "password",
        })
        repository = get_di_class(UserRepository)
        user = await repository.get_user_by_email("test@test.com")
        actual = response.json()
        
        assert user.is_active == True
        assert response.status_code == 200
        assert actual['data']['user']['token'] is not None
        actual["data"]["user"].pop("token")# tokenは存在確認で十分なので削除
        assert actual == {
            "status": 200,
            "data": {
                "user": {
                    "id": user.id,
                    "uuid": user.uuid,
                    "account_name": user.account_name,
                    "id_account": user.id_account,
                    "email": user.email,
                    "birth_date": user.birth_date.strftime("%Y-%m-%d"),
                    "other_user_invitation_code": user.other_user_invitation_code,
                    "refresh_token": user.refresh_token,
                    "expires_at": user.expires_at.isoformat(),
                    "deleted_at": None,
                    "created_at": user.created_at.isoformat(),
                    "updated_at": user.updated_at.isoformat(),
                },
            },
            "message": "ok"
        }
        
    @pytest.mark.asyncio
    async def test_sign_in_認証失敗時は401エラーを返す(self, async_client, setup_user):
        response = await async_client.post('/sign_in', data={
            "username": "dummy",
            "password": "dummy",
        })
        assert response.status_code == 401
        assert response.json() == {
            "error": "http-error",
            "status": 401,
            "message": "Unauthorized",
        }
        
    @pytest.mark.asyncio
    async def test_sign_out_サインアウトが成功する(self, async_client, setup_user, get_auth_user):
        user = get_auth_user
        headers = {"Authorization": f"Bearer {user.token}"}
        response = await async_client.post('/sign_out', headers=headers)
        
        assert response.status_code == 200
        assert response.json() == {"status": 200, "data": {"result": True}, "message": "ok"}
                
        repository = get_di_class(UserRepository)
        refresh_user = await repository.get_user_by_email(user.email)
        
        assert refresh_user.is_active == False
        assert refresh_user.refresh_token == None
        assert refresh_user.expires_at == None
        
    # サインアウト以上系
    # リフレッシュトークン系のテスト
    # リフレッシュトークンの異常系テスト
        
    
    @pytest.mark.asyncio
    async def test_email_exists_メールアドレスが存在したらtrueを返す(self, async_client, setup_user):        
        response = await async_client.post('/email-exists', json={"email": "test@test.com"})
        assert response.status_code == 200
        assert response.json()['data'] == {"exists": True}

    @pytest.mark.asyncio
    async def test_email_exists_メールアドレスが存在しなければfalseを返す(self, async_client, setup_user):    
        response = await async_client.post('/email-exists', json={"email": "non_test@test.com"})
        assert response.status_code == 200
        assert response.json()['data'] == {"exists": False}
        
    @pytest.mark.asyncio
    async def test_id_account_exists_アカウントIDが存在したらtrueを返す(self, async_client, setup_user):
        response = await async_client.post('/id-account-exists', json={"id_account": "test"})
        assert response.status_code == 200
        assert response.json()['data'] == {"exists": True}
        
    @pytest.mark.asyncio
    async def test_id_account_exists_アカウントIDが存在しなければfalseを返す(self, async_client, setup_user):    
        response = await async_client.post('/id-account-exists', json={"id_account": "non_test"})
        assert response.status_code == 200
        assert response.json()['data'] == {"exists": False}
    