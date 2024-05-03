import pytest
from httpx import AsyncClient

from app.resource.depends.depends import get_di_class
from app.resource.model.files import Files
from app.resource.repository.file_repository import FileRepository
from app.resource.repository.user_repository import UserRepository

# テストコマンド
# pytest -vv tests/feature/test_user_controller.py


class TestUserController:
    @pytest.mark.asyncio  # ユーザーが居ない場合はauthでテスト済みなので省略(current_userを返してるだけ)
    async def test_get_me_ユーザーが取得できる(self, async_client: AsyncClient, get_auth_user, get_header):
        user = get_auth_user
        headers = get_header
        headers["Authorization"] = f"Bearer {user.token}"
        response = await async_client.get("/me", headers=headers)
        actual = response.json()
        
        assert response.status_code == 200
        assert actual == {
            "status": 200,
            "data": {
                "user": {
                    "id": user.id,
                    "image_id": user.image_id,
                    "uuid": user.uuid,
                    "file": user.file,
                    "account_name": user.account_name,
                    "id_account": user.id_account,
                    "email": user.email,
                    "birth_date": user.birth_date.strftime("%Y-%m-%d"),
                    "other_user_invitation_code": user.other_user_invitation_code,
                    "expires_at": user.expires_at.isoformat(),
                    "email_verified": user.email_verified,
                    "profile": user.profile,
                    "link": user.link,
                    "deleted_at": user.deleted_at,
                    "created_at": user.created_at.isoformat(),
                    "updated_at": user.updated_at.isoformat(),
                },
            },
            "message": "ok",
        }
        
    @pytest.mark.asyncio
    async def test_get_me_プロフィール画像が登録済みの場合(self, async_client: AsyncClient, get_auth_user, get_header):
        user = get_auth_user
        headers = get_header
        headers["Authorization"] = f"Bearer {user.token}"
        # ファイル作成
        file = Files(
            name="string",
            path="string",
        )
        userRepository = get_di_class(UserRepository)
        fileRepository = get_di_class(FileRepository)
        saved_file = await fileRepository.create(files=[file])
        user = await userRepository.save_profile(
            user_uuid=user.uuid,
            image_id=saved_file[0].id
        )

        response = await async_client.get("/me", headers=headers)
        actual = response.json()
        
        assert response.status_code == 200
        assert actual == {
            "status": 200,
            "data": {
                "user": {
                    "id": user.id,
                    "image_id": user.image_id,
                    "uuid": user.uuid,
                    "file": {
                        "id": user.file.id,
                        "uuid": user.file.uuid,
                        "name": user.file.name,
                        "path": user.file.path,
                        "is_used": user.file.is_used,
                        "created_at": user.file.created_at.isoformat(),
                        "updated_at": user.file.updated_at.isoformat(),
                    },
                    "account_name": user.account_name,
                    "id_account": user.id_account,
                    "email": user.email,
                    "birth_date": user.birth_date.strftime("%Y-%m-%d"),
                    "other_user_invitation_code": user.other_user_invitation_code,
                    "expires_at": user.expires_at.isoformat(),
                    "email_verified": user.email_verified,
                    "profile": user.profile,
                    "link": user.link,
                    "deleted_at": user.deleted_at,
                    "created_at": user.created_at.isoformat(),
                    "updated_at": user.updated_at.isoformat(),
                },
            },
            "message": "ok",
        }

    @pytest.mark.asyncio
    async def test_save_user_profile_プロフィール画像を登録する(self, async_client: AsyncClient, get_auth_user, get_header):
        user = get_auth_user
        headers = get_header
        headers["Authorization"] = f"Bearer {user.token}"
        # ファイル作成
        file = Files(
            name="string",
            path="string",
        )
        fileRepository = get_di_class(FileRepository)
        saved_file = await fileRepository.create(files=[file])

        data = {
            "account_name": "test_account_name_dummy",
            "link": "https://example.com",
            "profile": "test_profile_dummy",
            "image_uuid": saved_file[0].uuid,  # ファイルのuuidで一致検索するため、uuidを指定
        }
        response = await async_client.post("/user/profile", headers=headers, json=data)
        actual = response.json()

        assert response.status_code == 200
        assert actual == {
            "status": 200,
            "data": None,
            "message": "ok",
        }

        userRepository = get_di_class(UserRepository)
        user = await userRepository.get_user_by_uuid(user.uuid)
        assert user.account_name == data["account_name"]
        assert user.link == data["link"]
        assert user.profile == data["profile"]
        assert user.image_id == saved_file[0].id
        
    @pytest.mark.asyncio
    async def test_save_user_profile_プロフィール画像を登録しない(self, async_client: AsyncClient, get_auth_user, get_header):
        user = get_auth_user
        headers = get_header
        headers["Authorization"] = f"Bearer {user.token}"
        data = {
            "account_name": "test_account_name_dummy",
            "link": "https://example.com",
            "profile": "test_profile_dummy",
        }
        response = await async_client.post("/user/profile", headers=headers, json=data)
        actual = response.json()

        assert response.status_code == 200
        assert actual == {
            "status": 200,
            "data": None,
            "message": "ok",
        }

        userRepository = get_di_class(UserRepository)
        user = await userRepository.get_user_by_uuid(user.uuid)
        assert user.account_name == data["account_name"]
        assert user.link == data["link"]
        assert user.profile == data["profile"]
        assert user.image_id is None
        
    @pytest.mark.asyncio
    async def test_save_user_profile_プロフィール画像を登録する_ファイルが存在しない場合(self, async_client: AsyncClient, get_auth_user, get_header):
        user = get_auth_user
        headers = get_header
        headers["Authorization"] = f"Bearer {user.token}"
        data = {
            "account_name": "test_account_name_dummy",
            "link": "https://example.com",
            "profile": "test_profile_dummy",
            "image_uuid": "dummy_uuid",
        }
        response = await async_client.post("/user/profile", headers=headers, json=data)
        actual = response.json()

        assert response.status_code == 400
        assert actual == {
            "detail": [
                {
                    "loc": ["POST /user/profile"],
                    "msg": "ファイルが存在しません",
                    "type": "http_error",
                }
            ],
        }