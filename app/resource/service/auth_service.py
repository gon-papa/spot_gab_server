from app.resource.repository.user_repository import UserRepository
from app.resource.service_domain.auth_service_domain import get_user

from injector import inject

class AuthService:
    @inject
    def __init__(self, repository: UserRepository):
        self.repository = repository

    # async def sign_up(self) -> dict:
    #     # ユーザー登録処理をここに実装
    #     return await self.repository.create_user()
    
    async def sign_in(self, email: str, password: str) -> dict:
        # ユーザー認証処理をここに実装
        return await get_user(user_repository=self.repository, email=email)
    
    async def email_exist(self, email: str) -> bool:
        return await self.repository.email_exist(email)
    
    async def id_account_exist(self, id_account: str) -> bool:
        return await self.repository.id_account_exist(id_account)
