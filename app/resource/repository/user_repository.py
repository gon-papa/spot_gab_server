from datetime import datetime
import re
from sqlalchemy.future import select
from app.db.db import get_db
from app.resource.model.users import Users
from sqlalchemy.orm import Session
from injector import inject
from typing import Optional

from app.resource.request.auth_request import SignUpRequest
import typing

class UserRepository:
    # ユーザー作成
    async def create_user(self, user:Users) -> Users:
        async with get_db() as session:
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    # emailの存在確認
    async def email_exist(self, email: str) -> bool:
        async with get_db() as session:
            result = await session.execute(select(Users).filter(Users.email == email))
            user = result.scalars().first()
            return user is not None
        
    # id_accountの存在確認
    async def id_account_exist(self, id_account: str) -> bool:
        async with get_db() as session:
            result = await session.execute(select(Users).filter(Users.id_account == id_account))
            user = result.scalars().first()
            return user is not None
        
    # emailからuser取得
    async def get_user_by_email(self, email: str) -> Optional[Users]:
        async with get_db() as session:
            result = await session.execute(select(Users).filter(Users.email == email))
            user = result.scalars().first()
            return user
        
    # uuidからuser取得
    async def get_user_by_uuid(self, uuid: str)-> Optional[Users]:
        async with get_db() as session:
            result = await session.execute(select(Users).filter(Users.uuid == uuid))
            user = result.scalars().first()
            return user
    
    # サインイン時にユーザーをアクティブ状態に更新(リフレッシュトークンと有効期限も更新)
    async def active_update(self, id: int, refresh_token: str, exp: datetime) -> Users:
        async with get_db() as session:
            result = await session.execute(select(Users).where(Users.id == id))
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
        async with get_db() as session:
            user.is_active = False
            user.refresh_token = None
            user.expires_at = None
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user
        