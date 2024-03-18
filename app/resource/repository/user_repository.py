from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select

from app.db.db import DatabaseConnection
from app.resource.depends.depends import get_di_class
from app.resource.model.email_verification import EmailVerification
from app.resource.model.password_reset_verifications import PasswordResetVerifications
from app.resource.model.users import Users


class UserRepository:
    def __init__(self) -> None:
        self.db = get_di_class(DatabaseConnection)

    # ユーザー作成
    async def create_user(self, user: Users) -> Users:
        async with self.db.get_db() as session:
            try:
                session.add(user)
                await session.commit()
                await session.refresh(user)
                return user
            except SQLAlchemyError as e:
                session.rollback()
                raise e

    # emailの存在確認
    async def email_exist(self, email: str) -> bool:
        async with self.db.get_db() as session:
            result = await session.exec(select(Users).filter(Users.email == email))
            user = result.scalars().first()
            return user is not None

    # id_accountの存在確認
    async def id_account_exist(self, id_account: str) -> bool:
        async with self.db.get_db() as session:
            result = await session.exec(select(Users).filter(Users.id_account == id_account))
            user = result.scalars().first()
            return user is not None

    # idからuser取得
    async def get_user_by_id(self, id: int) -> Optional[Users]:
        async with self.db.get_db() as session:
            result = await session.exec(select(Users).filter(Users.id == id))
            user = result.scalars().first()
            return user

    # emailからuser取得
    async def get_user_by_email(self, email: str) -> Optional[Users]:
        async with self.db.get_db() as session:
            result = await session.exec(select(Users).filter(Users.email == email))
            user = result.scalars().first()
            return user

    # uuidからuser取得
    async def get_user_by_uuid(self, uuid: str) -> Optional[Users]:
        async with self.db.get_db() as session:
            result = await session.exec(select(Users).filter(Users.uuid == uuid))
            user = result.scalars().first()
            return user

    # サインイン時にユーザーをアクティブ状態に更新(リフレッシュトークンと有効期限も更新)
    async def active_update(self, id: int, refresh_token: str, exp: datetime) -> Users:
        async with self.db.get_db() as session:
            result = await session.exec(select(Users).where(Users.id == id))
            user = result.scalars().first()
            user.is_active = True
            user.refresh_token = refresh_token
            user.expires_at = exp
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    # サインアウト時にユーザーを非アクティブ状態に更新(リフレッシュトークンと有効期限も削除)
    async def inactive_update(self, user: Users) -> Users:
        async with self.db.get_db() as session:
            user.is_active = False
            user.refresh_token = None
            user.expires_at = None
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    # リフレッシュトークンからユーザー取得
    async def get_user_by_refresh_token(self, refresh_token: str) -> Optional[Users]:
        async with self.db.get_db() as session:
            result = await session.exec(
                select(Users).filter(
                    Users.refresh_token == refresh_token, Users.expires_at > datetime.now(timezone.utc)
                )
            )
            user = result.scalars().first()
            return user

    # email認証後のアップデート
    async def email_verify_update(self, user: Users, ev: EmailVerification) -> Users:
        async with self.db.get_db() as session:
            try:
                user.email_verified = True
                ev.email_verified_at = datetime.now(timezone.utc)
                ev.email_verify_token = None
                ev.email_verified_expired_at = None
                session.add(user)
                session.add(ev)
                await session.commit()
                await session.refresh(user)
                return user
            except SQLAlchemyError as e:
                session.rollback()
                raise e

    # パスワード更新
    async def password_reset_update(
        self,
        user: Users,
        pr: PasswordResetVerifications,
        hashed_password: str
    ) -> Users:
        async with self.db.get_db() as session:
            user.hashed_password = hashed_password
            pr.verify_token = None
            pr.verified_expired_at = None
            try:
                session.add(user)
                session.add(pr)
                await session.commit()
                await session.refresh(user)
                return user
            except SQLAlchemyError as e:
                session.rollback()
                raise e
