from fastapi import UploadFile, File
import os
from dotenv import load_dotenv

from app.resource.util.storage.local_storage import LocalStorage
from app.resource.util.storage.s3_storage import S3Storage

load_dotenv()


class StorageUtil:
    def __init__(self):
        self.env = os.getenv("ENV", "development")

    async def upload_file(self, uuid: str, file: UploadFile = File(...)) -> str:
        file_path = f"{uuid}"
        if self.env == "development":
            return await LocalStorage().save_file(file, uuid)
        else:
            return await S3Storage().save_file_s3(file, file_path)


storageUtil = StorageUtil()
