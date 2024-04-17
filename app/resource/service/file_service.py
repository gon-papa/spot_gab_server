

from typing import List
from fastapi import File
from injector import inject

from app.resource.model.files import Files
from app.resource.repository.file_repository import FileRepository
from app.resource.util.storage.storage import StorageUtil


class FileService:
    @inject
    def __init__(
        self,
        repository: FileRepository,
    ) -> None:
        self.repository = repository

    async def create(self, files: List[File], user_uuid: str) -> List[Files]:
        # 繰り返し
        file_objects = []
        for file in files:
            name = file.filename is not None and file.filename or "none"
            path = await StorageUtil().upload_file(user_uuid, file)
            file = Files(
                name=name,
                path=path,
            )
            file_objects.append(file)

        return await self.repository.create(file_objects)
