import os
from dotenv import load_dotenv
from fastapi import UploadFile
import logging

load_dotenv()
logger = logging.getLogger("app.exception")


class LocalStorage:
    def __init__(self) -> None:
        self.dir_base_path = "app/public/upload_files"
        self.base_url = os.getenv("BASE_URL", "http://localhost:8000")
        self.http_access_base_path = f"{self.base_url}/public/upload_files"

    async def save_file(self, file: UploadFile, uuid: str) -> str:
        try:
            file_name = file.filename
            # ディレクトリパスを構築(uuidごとにディレクトリを作成する)
            dir_path = os.path.dirname(f"{self.dir_base_path}/{uuid}/")
            # ディレクトリが存在しない場合は作成
            os.makedirs(dir_path, exist_ok=True)
            # ファイル保存フルパス(ファイル名含む)
            save_path = f"{self.dir_base_path}/{uuid}/{file_name}"
            with open(save_path, "wb") as buffer:
                buffer.write(file.file.read())
            # 返すパスはhttpアクセス可能なパス
            return f"{self.http_access_base_path}/{uuid}/{file_name}"
        except Exception:
            logger.error(Exception)
            raise Exception("ファイルの保存に失敗しました。")
