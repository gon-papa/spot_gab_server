from sqlalchemy.future import select
from app.db.db import get_db
from app.resource.model.users import Users
from sqlalchemy.orm import Session
from injector import inject

class UserRepository:
    async def create_user(self) -> dict:
        # ここにユーザー作成のロジックを実装
        return {"message": "Create user repository"}

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
        
    # uuidからuser取得
    async def get_user_by_email(self, email: str) -> Users:
        async with get_db() as session:
            result = await session.execute(select(Users).filter(Users.email == email))
            user = result.scalars().first()
            return user