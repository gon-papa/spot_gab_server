from app.db.db import DatabaseConnection
from app.resource.depends.depends import get_di_class
from app.resource.model.email_verification import EmailVerification
from sqlalchemy.future import select


class EmailVerificationRepository:
    def __init__(self) -> None:
        self.db = get_di_class(DatabaseConnection)

    # email_verify_tokenからemail_verification取得
    async def get_email_verification_by_token(self, token: str) -> EmailVerification:
        async with self.db.get_db() as session:
            result = await session.exec(select(EmailVerification).filter(EmailVerification.email_verify_token == token))
            email_verification = result.scalars().first()
            return email_verification
        
    # user_idからemail_verification取得
    async def get_email_verification_by_user_id(self, user_id: int) -> EmailVerification:
        async with self.db.get_db() as session:
            result = await session.exec(select(EmailVerification).filter(EmailVerification.user_id == user_id))
            email_verification = result.scalars().first()
            return email_verification
