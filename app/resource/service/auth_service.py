from datetime import datetime, timedelta
import os
from app.resource.depends.depends import get_di_class
from app.resource.repository.email_varification_repository import EmailVerificationRepository
from app.resource.repository.user_repository import UserRepository
from app.resource.service_domain.auth_service_domain import (
    authenticate_user,
    get_password_hash,
    create_refresh_token,
    create_expire_at,
    crate_user_claim,
    create_access_token
)
from fastapi import HTTPException, BackgroundTasks
from injector import inject
from app.resource.request.auth_request import SignUpRequest
from app.resource.model.users import SignUpUser, Users
from app.resource.model.email_verification import EmailVerification
from app.resource.util.mailer.templetes.verify_email import VerifyEmail
from app.resource.util.mailer.mailer import Mailer

class AuthService:
    @inject
    def __init__(self, repository: UserRepository, emailVerificationRepository: EmailVerificationRepository):
        self.repository = repository
        self.emailVerificationRepository = emailVerificationRepository        

    # サインアップ
    async def sign_up(self, request:SignUpRequest, bk: BackgroundTasks) -> SignUpUser:
        is_email_exist = await self.email_exist(request.email)
        is_id_account_exist = await self.id_account_exist(request.id_account)
        if is_email_exist:
            raise HTTPException(status_code=400, detail="Email already registered")
        if is_id_account_exist:
            raise HTTPException(status_code=400, detail="Account ID already registered")

        email_verify_token = create_refresh_token()
        user = Users(
            account_name = request.account_name,
            id_account = request.id_account,
            email = request.email,
            hashed_password = get_password_hash(request.password),
            birth_date = request.birth_date,
            is_active = True,
            refresh_token = create_refresh_token(),
            expires_at = create_expire_at(),
            email_verifications = EmailVerification(
                email_verify_token = email_verify_token,
                email_verified_expired_at = datetime.utcnow() + timedelta(days=1),
            )
        )
        user = await self.repository.create_user(user)
        # アクセストークン作成
        claim = crate_user_claim(user)
        token = create_access_token(claim)
        user = SignUpUser.model_validate(user)
        user.token = token
        # 認証メール送付
        template = get_di_class(VerifyEmail).get_html(
            email_verify_token,
            user.account_name,
            os.getenv('SUPPORT_URL')
        )
        bk.add_task(
            get_di_class(Mailer).send,
            subject="メールアドレスの確認",
            to=[user.email],
            body=template
        )
        return user
    
    # サインイン
    async def sign_in(self, email: str, password: str) -> dict:
        # emailとpasswordが一致するユーザーを取得
        user = await authenticate_user(email, password)
        if not user:
            raise HTTPException(status_code=403, detail="Incorrect email or password")
        # アクセストークン作成
        claim = crate_user_claim(user)
        token = create_access_token(claim)
        # リフレッシュトークンの有効期限作成
        refresh_token = create_refresh_token()
        expires_at = create_expire_at()
        user = await self.repository.active_update(user.id, refresh_token, expires_at)
        return {'token': token, 'refresh_token': refresh_token}
    
    # サインアウト
    async def sign_out(self, user: Users) -> bool:
        user = await self.repository.inactive_update(user)
        if user is None:
            return False
        return True
    
    # リフレッシュトークンユーザー認証
    async def get_refresh_token(self, token: str)-> SignUpUser:
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
        user = SignUpUser.model_validate(user)
        user.token = token
        return user   
    
    # email存在チェック
    async def email_exist(self, email: str) -> bool:
        return await self.repository.email_exist(email)
    
    # アカウントID存在チェック
    async def id_account_exist(self, id_account: str) -> bool:
        return await self.repository.id_account_exist(id_account)

    # メール認証
    async def email_verify(self, token: str) -> dict:
        ev = await self.emailVerificationRepository.get_email_verification_by_token(token)
        if ev is None:
            raise HTTPException(status_code=400, detail="Invalid token")
        if ev.email_verified_expired_at < datetime.utcnow():
            raise HTTPException(status_code=400, detail="Expired token")
        user = await self.repository.get_user_by_id(ev.user_id)
        if user is None:
            raise HTTPException(status_code=400, detail="User not found")
        if user.email_verified:
            raise HTTPException(status_code=400, detail="Already verified")
        # 認証保存処理
        await self.repository.email_verify_update(user, ev)
        
        return {"result": True, "detail": "Email verified"}