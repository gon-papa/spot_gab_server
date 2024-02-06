from app.resource.repository.user_repository import UserRepository
from injector import inject

class AuthService:
    @inject
    def __init__(self, repository: UserRepository):
        self.repository = repository

    # async def sign_up(self) -> dict:
    #     # ユーザー登録処理をここに実装
    #     return await self.repository.create_user()
    
    async def email_exist(self, email: str) -> bool:
        return await self.repository.email_exist(email)
