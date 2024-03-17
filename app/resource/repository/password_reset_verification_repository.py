from app.db.db import DatabaseConnection
from app.resource.depends.depends import get_di_class
from app.resource.model.password_reset_verifications import PasswordResetVerifications
from sqlalchemy.future import select


class PasswordResetVerificationRepository:
    def __init__(self) -> None:
        self.db = get_di_class(DatabaseConnection)

    # パスワードリセットトークンを登録
    async def create_password_reset_verification(
        self,
        password_reset_verification: PasswordResetVerifications
    ) -> PasswordResetVerifications:
        async with self.db.get_db() as session:
            result = await session.execute(
                select(PasswordResetVerifications).where(
                    PasswordResetVerifications.user_id == password_reset_verification.user_id
                )
            )
            data = result.scalar_one_or_none()
            
            if data is None:
                session.add(password_reset_verification)
            else:
                data.verify_token = password_reset_verification.verify_token
                data.verified_expired_at = password_reset_verification.verified_expired_at
                session.add(data)

            await session.commit()
            await session.refresh(data)
            return data
        
    async def get_by_token(self, token: str) -> PasswordResetVerifications:
        async with self.db.get_db() as session:
            result = await session.execute(
                select(PasswordResetVerifications).where(
                    PasswordResetVerifications.verify_token == token
                )
            )
            return result.scalar_one_or_none()
