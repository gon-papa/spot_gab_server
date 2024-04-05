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

    async def save_profile(self, user: Users, profile: str, image_data: bytes) -> Users:
        image_path = None
        # 画像保存処理
        if image_data is not None:
            # 画像保存処理
            image_path = await storageUtil.upload_file(user.uuid, image_data)

        return await self.repository.save_profile(user.uuid, profile, image_path)
