import boto3
from botocore.exceptions import NoCredentialsError
import os
from dotenv import load_dotenv
from fastapi import UploadFile, HTTPException

load_dotenv()


class S3Storage:
    def __init__(self) -> None:
        self.bucket_name = os.getenv("S3_BUCKET_NAME")
        self.aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

    async def save_file_s3(self, file: UploadFile, file_path: str):
        s3 = boto3.client(
            "s3", aws_access_key_id=self.aws_access_key, aws_secret_access_key=self.aws_secret_access_key
        )
        try:
            s3.upload_fileobj(file.file, self.bucket_name, file_path)
            return f"https://{self.bucket_name}.s3.amazonaws.com/{file_path}"
        except NoCredentialsError:
            raise HTTPException(status_code=500, detail="Could not connect to S3")
