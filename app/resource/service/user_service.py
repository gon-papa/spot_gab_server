import logging
from fastapi import HTTPException
from injector import inject
from app.resource.model.users import Users
from app.resource.repository.file_repository import FileRepository
from app.resource.repository.user_repository import UserRepository
from app.resource.request.user_request import UserProfileRequest

logger = logging.getLogger("app.exception")


class UserService:
    @inject
    def __init__(
        self,
        repository: UserRepository,
        fileRepository: FileRepository,
    ):
        self.repository = repository
        self.fileRepository = fileRepository

    async def get_user(self, uuid: str) -> Users:
        # TODO フォロー、フォロワー数も入れ込む
        return await self.repository.get_user_by_uuid(uuid)

    async def save_profile(
        self,
        user: Users,
        request: UserProfileRequest,
    ) -> Users:
        file = None
        if (request.image_uuid is not None) and (request.image_uuid != ""):
            file = await self.fileRepository.findByUuid(request.image_uuid)
            if file is None:
                raise HTTPException(status_code=400, detail="ファイルが存在しません")
        return await self.repository.save_profile(
            user.uuid,
            request.account_name,
            request.link,
            request.profile,
            file.id if file else None,
        )
