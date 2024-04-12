from typing import Optional
from fastapi import File
from injector import inject
from app.resource.model.users import Users
from app.resource.repository.user_repository import UserRepository
from app.resource.util.storage.storage import storageUtil


class UserService:
    @inject
    def __init__(
        self,
        repository: UserRepository,
    ):
        self.repository = repository

    async def get_user(self, uuid: str) -> Users:
        # TODO フォロー、フォロワー数も入れ込む
        return await self.repository.get_user_by_uuid(uuid)

    async def save_profile(
        self,
        user: Users,
        accountName: Optional[str],
        link: Optional[str],
        profile: Optional[str],
        image_data: File = None,
    ) -> Users:
        image_path = None
        # 画像保存処理
        if image_data is not None:
            # 画像保存処理
            image_path = await storageUtil.upload_file(user.uuid, image_data)

        # 全てNoneならそのままReturn
        if accountName is None and link is None and profile is None and image_path is None:
            return user

        return await self.repository.save_profile(user.uuid, accountName, link, profile, image_path)
