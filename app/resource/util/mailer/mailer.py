import os
from typing import List

from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from pydantic import EmailStr

load_dotenv()


class Mailer:
    def __init__(self):
        self.conf = ConnectionConfig(
            MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
            MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
            MAIL_FROM=os.getenv("MAIL_FROM"),
            MAIL_PORT=os.getenv("MAIL_PORT"),
            MAIL_SERVER=os.getenv("MAIL_SERVER"),
            MAIL_FROM_NAME=os.getenv("MAIL_FROM_NAME"),
            MAIL_STARTTLS=os.getenv("MAIL_STARTTLS"),
            MAIL_SSL_TLS=os.getenv("MAIL_SSL_TLS"),
            USE_CREDENTIALS=os.getenv("USE_CREDENTIALS"),
            VALIDATE_CERTS=os.getenv("VALIDATE_CERTS"),
        )
        self.mail = FastMail(self.conf)

    async def send(self, to: List[EmailStr], subject: str, body: str) -> bool:
        try:
            message = MessageSchema(
                subject=subject, recipients=to, body=body, subtype="html"  # List of recipients, as EmailStr type
            )

            await self.mail.send_message(message)
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def str_to_bool(s: str) -> bool:
        return s.lower() in ("true", "True")
