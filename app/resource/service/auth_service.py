from datetime import datetime, timedelta
from app.resource.repository.user_repository import UserRepository
from app.resource.service_domain.auth_service_domain import (
    authenticate_user,
    get_password_hash,
    create_refresh_token,
    create_expire_at,
    crate_user_claim,
    create_access_token
)

from fastapi import HTTPException
from injector import inject
from app.resource.request.auth_request import SignUpRequest
from app.resource.model.users import SignInUser, Users

class AuthService:
    @inject
    def __init__(self, repository: UserRepository):
        self.repository = repository
    # サインアップ
    async def sign_up(self, request:SignUpRequest) -> SignInUser:
        is_email_exist = await self.email_exist(request.email)
        is_id_account_exist = await self.id_account_exist(request.id_account)
        if is_email_exist:
            raise HTTPException(status_code=400, detail="Email already registered")
        if is_id_account_exist:
            raise HTTPException(status_code=400, detail="Account ID already registered")
        user = Users(
            account_name = request.account_name,
            id_account = request.id_account,
            email = request.email,
            hashed_password = get_password_hash(request.password),
            birth_date = request.birth_date,
            is_active = True,
            refresh_token = create_refresh_token(),
            expires_at = create_expire_at(),
            email_verify_token=create_refresh_token(),
            email_verified_expired_at=datetime.utcnow() + timedelta(days=1)
        )
        user = await self.repository.create_user(user)
        # アクセストークン作成
        claim = crate_user_claim(user)
        token = create_access_token(claim)
        user = SignInUser.model_validate(user)
        user.token = token
        return user
    
    # サインイン
    async def sign_in(self, email: str, password: str) -> SignInUser:
        # emailとpasswordが一致するユーザーを取得
        user = await authenticate_user(email, password)
        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized")
        # アクセストークン作成
        claim = crate_user_claim(user)
        token = create_access_token(claim)
        # リフレッシュトークンの有効期限作成
        refresh_token = create_refresh_token()
        expires_at = create_expire_at()
        user = await self.repository.active_update(user.id, refresh_token, expires_at)
        user = SignInUser.model_validate(user)
        user.token = token
        return user   
    
    # サインアウト
    async def sign_out(self, user: Users) -> bool:
        user = await self.repository.inactive_update(user)
        if user is None:
            return False
        return True
    
    # リフレッシュトークンユーザー認証
    async def get_refresh_token(self, token: str)-> SignInUser:
        user = await self.repository.get_user_by_refresh_token(token)
        if user is None:
            raise HTTPException(status_code=401, detail="Unauthorized")
        if not user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        if user.deleted_at is not None:
            raise HTTPException(status_code=400, detail="Deleted user")
        # アクセストークン作成
        claim = crate_user_claim(user)
        token = create_access_token(claim)
        # リフレッシュトークンの有効期限作成
        refresh_token = create_refresh_token()
        expires_at = create_expire_at()
        user = await self.repository.active_update(user.id, refresh_token, expires_at)
        user = SignInUser.model_validate(user)
        user.token = token
        return user   
    
    # email存在チェック
    async def email_exist(self, email: str) -> bool:
        return await self.repository.email_exist(email)
    
    # アカウントID存在チェック
    async def id_account_exist(self, id_account: str) -> bool:
        return await self.repository.id_account_exist(id_account)
