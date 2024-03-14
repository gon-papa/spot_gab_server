from datetime import date, datetime, timedelta, timezone

import pytest
import pytest_asyncio
from httpx import AsyncClient

from app.resource.depends.depends import get_di_class
from app.resource.model.email_verification import EmailVerification
from app.resource.model.users import Users
from app.resource.repository.email_varification_repository import EmailVerificationRepository
from app.resource.repository.user_repository import UserRepository
from app.resource.service_domain.auth_service_domain import create_refresh_token

# テストコマンド
# pytest tests/feature/test_auth_controller.py


class TestAuthController:
    @pytest_asyncio.fixture
    async def setup_user(self):
        self.user = Users(
            account_name="test",
            id_account="test",
            email="test@test.com",
            hashed_password="$2b$12$VUJv82tezCvUccA35HleFulwc4qYrz7BqFHIdK7yXQK0nEPyl2Cc.",  # password
            birth_date=date(2000, 1, 1),
            is_active=True,
            refresh_token="test",
            expires_at=datetime(2000, 1, 1, tzinfo=timezone.utc),
            email_verified=True,
        )
        repository = get_di_class(UserRepository)
        await repository.create_user(self.user)

    @pytest.mark.asyncio
    async def test_sign_up_サインアップが成功する(self, async_client: AsyncClient, mocker, get_header):
        mock_mail_send = mocker.patch("app.resource.util.mailer.mailer.Mailer.send", return_value=True)
        response = await async_client.post(
            "/sign-up",
            json={
                "account_name": "test_name",
                "id_account": "test_account_id",
                "email": "signup@test.com",
                "password": "Password",
                "birth_date": "2024-02-19",
            },
            headers=get_header,
        )
        repository = get_di_class(UserRepository)
        emailVarificationRepository = get_di_class(EmailVerificationRepository)
        user = await repository.get_user_by_email("signup@test.com")
        ev = await emailVarificationRepository.get_email_verification_by_user_id(user.id)
        actual = response.json()

        # レスポンス確認
        assert response.status_code == 200
        assert actual["data"]["user"]["token"] is not None
        actual["data"]["user"].pop("token")  # tokenは存在確認で十分なので削除
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
                    "email_verified": user.email_verified,
                    "deleted_at": None,
                    "created_at": user.created_at.isoformat(),
                    "updated_at": user.updated_at.isoformat(),
                },
            },
            "message": "ok",
        }
        # ユーザー確認
        assert user.is_active == True
        # email_varificationが作成されていること
        assert user.email_verified == False
        assert ev.user_id == user.id
        assert ev.email_verify_token is not None
        assert ev.email_verified_expired_at is not None
        assert ev.email_verified_at == None
        # メール送信がされていること
        mock_mail_send.assert_called_once()
        call_args = mock_mail_send.call_args[1]
        assert call_args["to"] == ["signup@test.com"]
        assert "メールアドレスの確認" == call_args["subject"]

    @pytest.mark.asyncio
    async def test_sign_up_メールアドレスが登録済みなら400エラーを返す(self, async_client, setup_user, get_header):
        response = await async_client.post(
            "/sign-up",
            json={
                "account_name": "test_name",
                "id_account": "test_account_id",
                "email": "test@test.com",
                "password": "Password",
                "birth_date": "2024-02-19",
            },
            headers=get_header,
        )
        assert response.status_code == 400
        assert response.json() == {
            "detail": [
                {
                    "loc": [
                        "POST /sign-up",
                    ],
                    "msg": "このメールアドレスは利用できません",
                    "type": "http_error",
                }
            ]
        }

    @pytest.mark.asyncio
    async def test_sign_up_アカウントIDが登録済みなら400エラーを返す(self, async_client, setup_user, get_header):
        response = await async_client.post(
            "/sign-up",
            json={
                "account_name": "test_name",
                "id_account": "test",
                "email": "signup@test.com",
                "password": "Password",
                "birth_date": "2024-02-19",
            },
            headers=get_header,
        )
        assert response.status_code == 400
        assert response.json() == {
            "detail": [
                {
                    "loc": [
                        "POST /sign-up",
                    ],
                    "msg": "このアカウントIDは利用できません",
                    "type": "http_error",
                }
            ]
        }

    @pytest.mark.asyncio
    async def test_sign_in_サインインが成功する(self, async_client, setup_user, get_header):
        response = await async_client.post(
            "/sign-in",
            data={
                "username": "test@test.com",
                "password": "password",
            },
            headers=get_header,
        )
        repository = get_di_class(UserRepository)
        user = await repository.get_user_by_email("test@test.com")
        actual = response.json()

        assert user.is_active == True
        assert response.status_code == 200
        assert actual["access_token"] is not None
        assert actual["token_type"] == "bearer"

    @pytest.mark.asyncio
    async def test_sign_in_認証失敗時は403エラーを返す(self, async_client, setup_user, get_header):
        response = await async_client.post(
            "/sign-in",
            data={
                "username": "dummy",
                "password": "dummy",
            },
            headers=get_header,
        )
        assert response.status_code == 403
        assert response.json() == {
            "detail": [
                {
                    "loc": [
                        "POST /sign-in",
                    ],
                    "msg": "メールアドレスかパスワードが間違っています",
                    "type": "http_error",
                }
            ]
        }

    @pytest.mark.asyncio
    async def test_sign_out_サインアウトが成功する(self, async_client, setup_user, get_auth_user, get_header):
        user = get_auth_user
        headers = get_header
        headers["Authorization"] = f"Bearer {user.token}"
        response = await async_client.post("/sign-out", headers=headers)

        assert response.status_code == 200
        assert response.json() == {"status": 200, "data": {"result": True}, "message": "ok"}

        repository = get_di_class(UserRepository)
        refresh_user = await repository.get_user_by_email(user.email)

        assert refresh_user.is_active == False
        assert refresh_user.refresh_token == None
        assert refresh_user.expires_at == None

    @pytest.mark.asyncio
    async def test_sign_out_サインアウト_サインアウト後のユーザーは400エラー(
        self, async_client, setup_user, get_auth_user, get_header
    ):
        user = get_auth_user
        user.is_active = False
        repository = get_di_class(UserRepository)
        await repository.inactive_update(user)
        headers = get_header
        headers["Authorization"] = f"Bearer {user.token}"
        response = await async_client.post("/sign-out", headers=headers)

        assert response.status_code == 400
        assert response.json() == {
            "detail": [
                {
                    "loc": [
                        "POST /sign-out",
                    ],
                    "msg": "すでにログアウト済みです",
                    "type": "http_error",
                }
            ]
        }

    @pytest.mark.asyncio
    async def test_sign_out_サインアウト_認証前のユーザーは401エラー(
        self, async_client, setup_user, get_auth_user, get_header
    ):
        response = await async_client.post("/sign-out", headers=get_header)

        assert response.status_code == 401
        assert response.json() == {
            "detail": [
                {
                    "loc": [
                        "POST /sign-out",
                    ],
                    "msg": "Not authenticated",
                    "type": "http_error",
                }
            ]
        }

    @pytest.mark.asyncio
    async def test_refresh_token_リフレッシュトークンが成功する(
        self, async_client, setup_user, get_auth_user, get_header
    ):
        user = get_auth_user
        response = await async_client.post(
            "/refresh-token", json={"refresh_token": user.refresh_token}, headers=get_header
        )

        assert response.status_code == 200
        assert response.json()["data"]["user"]["token"] is not None
        assert response.json()["data"]["user"]["refresh_token"] is not None
        assert response.json()["data"]["user"]["expires_at"] is not None
        assert user.refresh_token != response.json()["data"]["user"]["refresh_token"]  # 更新されていること

    @pytest.mark.asyncio
    async def test_email_exists_メールアドレスが存在したらtrueを返す(self, async_client, setup_user, get_header):
        response = await async_client.post("/email-exists", json={"email": "test@test.com"}, headers=get_header)
        assert response.status_code == 200
        assert response.json()["data"] == {"exists": True}

    @pytest.mark.asyncio
    async def test_email_exists_メールアドレスが存在しなければfalseを返す(self, async_client, setup_user, get_header):
        response = await async_client.post("/email-exists", json={"email": "non_test@test.com"}, headers=get_header)
        assert response.status_code == 200
        assert response.json()["data"] == {"exists": False}

    @pytest.mark.asyncio
    async def test_id_account_exists_アカウントIDが存在したらtrueを返す(self, async_client, setup_user, get_header):
        response = await async_client.post("/id-account-exists", json={"id_account": "test"}, headers=get_header)
        assert response.status_code == 200
        assert response.json()["data"] == {"exists": True}

    @pytest.mark.asyncio
    async def test_id_account_exists_アカウントIDが存在しなければfalseを返す(
        self, async_client, setup_user, get_header
    ):
        response = await async_client.post("/id-account-exists", json={"id_account": "non_test"}, headers=get_header)
        assert response.status_code == 200
        assert response.json()["data"] == {"exists": False}

    @pytest.mark.asyncio
    async def test_email_verify_メールアドレスの確認が成功すれば成功ページを返す(self, async_client, setup_user):
        email_verify_token = create_refresh_token()
        user = Users(
            account_name="test",
            id_account="test2",
            email="test2@test.com",
            hashed_password="$2b$12$VUJv82tezCvUccA35HleFulwc4qYrz7BqFHIdK7yXQK0nEPyl2Cc.",  # password
            birth_date=date(2000, 1, 1),
            is_active=True,
            refresh_token="test",
            expires_at=datetime(2030, 1, 1, tzinfo=timezone.utc),
            email_verified=False,
            email_verifications=EmailVerification(
                email_verify_token=email_verify_token,
                email_verified_expired_at=datetime.now(timezone.utc) + timedelta(days=1),
            ),
        )
        user = await get_di_class(UserRepository).create_user(user)

        response = await async_client.get(f"/verify-email/{email_verify_token}/ja")
        user = await get_di_class(UserRepository).get_user_by_id(user.id)
        ev = await get_di_class(EmailVerificationRepository).get_email_verification_by_user_id(user.id)
        assert response.status_code == 200
        assert "<h2>認証完了のお知らせ</h2>" in response.text
        assert user.email_verified == True
        assert ev.email_verified_at is not None
        assert ev.email_verify_token == None
        assert ev.email_verified_expired_at == None

    @pytest.mark.asyncio
    async def test_email_verify_メールアドレスの確認_認証済みの場合はエラーページを返す(
        self, async_client, setup_user
    ):
        email_verify_token = create_refresh_token()
        user = Users(
            account_name="test",
            id_account="test2",
            email="test2@test.com",
            hashed_password="$2b$12$VUJv82tezCvUccA35HleFulwc4qYrz7BqFHIdK7yXQK0nEPyl2Cc.",  # password
            birth_date=date(2000, 1, 1),
            is_active=True,
            refresh_token="test",
            expires_at=date(2000, 1, 1),
            email_verified=True,
            email_verifications=EmailVerification(
                email_verify_token=email_verify_token,
                email_verified_expired_at=datetime.now(timezone.utc) + timedelta(days=1),
            ),
        )
        user = await get_di_class(UserRepository).create_user(user)

        response = await async_client.get(f"/verify-email/{email_verify_token}/ja")
        assert response.status_code == 200
        assert "<h1>認証エラーのお知らせ</h1>" in response.text

    @pytest.mark.asyncio
    async def test_email_verify_メールアドレスの確認_期限切れの場合はエラーページを返す(
        self, async_client, setup_user
    ):
        email_verify_token = create_refresh_token()
        user = Users(
            account_name="test",
            id_account="test2",
            email="test2@test.com",
            hashed_password="$2b$12$VUJv82tezCvUccA35HleFulwc4qYrz7BqFHIdK7yXQK0nEPyl2Cc.",  # password
            birth_date=date(2000, 1, 1),
            is_active=True,
            refresh_token="test",
            expires_at=date(2000, 1, 1),
            email_verified=False,
            email_verifications=EmailVerification(
                email_verify_token=email_verify_token,
                email_verified_expired_at=datetime.now(timezone.utc) - timedelta(days=1),
            ),
        )

        user = await get_di_class(UserRepository).create_user(user)

        response = await async_client.get(f"/verify-email/{email_verify_token}/ja")
        assert response.status_code == 200
        assert "<h1>認証エラーのお知らせ</h1>" in response.text

    @pytest.mark.asyncio
    async def test_email_verify_メールアドレスの確認_トークンが存在しない場合はエラーページを返す(
        self, async_client, setup_user
    ):
        email_verify_token = create_refresh_token()
        user = Users(
            account_name="test",
            id_account="test2",
            email="test2@test.com",
            hashed_password="$2b$12$VUJv82tezCvUccA35HleFulwc4qYrz7BqFHIdK7yXQK0nEPyl2Cc.",  # password
            birth_date=date(2000, 1, 1),
            is_active=True,
            refresh_token="test",
            expires_at=date(2000, 1, 1),
            email_verified=False,
        )

        user = await get_di_class(UserRepository).create_user(user)
        response = await async_client.get(f"/verify-email/{email_verify_token}/ja")
        assert response.status_code == 200
        assert "<h1>認証エラーのお知らせ</h1>" in response.text
