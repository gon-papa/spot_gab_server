import os
from datetime import datetime, timedelta, timezone

from fastapi import BackgroundTasks, HTTPException
from injector import inject

from app.resource.depends.depends import get_di_class
from app.resource.model.email_verification import EmailVerification
from app.resource.model.users import SignUpUser, Users
from app.resource.repository.email_varification_repository import EmailVerificationRepository
from app.resource.repository.user_repository import UserRepository
from app.resource.request.auth_request import SignUpRequest
from app.resource.service_domain.auth_service_domain import (
    authenticate_user,
    crate_user_claim,
    create_access_token,
    create_expire_at,
    create_refresh_token,
    get_password_hash,
)
from app.resource.util.lang import convert_lang, get_current_language
from app.resource.util.mailer.mailer import Mailer
from app.resource.util.mailer.templetes.verify_email import VerifyEmail


class AuthService:
    @inject
    def __init__(self, repository: UserRepository, emailVerificationRepository: EmailVerificationRepository):
        self.repository = repository
        self.emailVerificationRepository = emailVerificationRepository

    # サインアップ
    async def sign_up(self, request: SignUpRequest, bk: BackgroundTasks) -> SignUpUser:
        is_email_exist = await self.email_exist(request.email)
        is_id_account_exist = await self.id_account_exist(request.id_account)
        if is_email_exist:
            raise HTTPException(status_code=400, detail=convert_lang("auth.error.exsist_email"))
        if is_id_account_exist:
            raise HTTPException(status_code=400, detail=convert_lang("auth.error.exsist_id_account"))

        email_verify_token = create_refresh_token()
        user = Users(
            account_name=request.account_name,
            id_account=request.id_account,
            email=request.email,
            hashed_password=get_password_hash(request.password),
            birth_date=request.birth_date,
            is_active=True,
            refresh_token=create_refresh_token(),
            expires_at=create_expire_at(),
            email_verifications=EmailVerification(
                email_verify_token=email_verify_token,
                email_verified_at=None,
                email_verified_expired_at=datetime.now(timezone.utc) + timedelta(days=1),
            ),
            deleted_at=None,
            email_verified=False,
        )
        user = await self.repository.create_user(user)
        # アクセストークン作成
        claim = crate_user_claim(user)
        token = create_access_token(claim)
        user = SignUpUser.model_validate(user)
        user.token = token
        # 認証メール送付
        if get_current_language() == "en":
            template = get_di_class(VerifyEmail).get_html_en(
                email_verify_token, user.account_name, os.getenv("SUPPORT_URL")
            )
        else:
            template = get_di_class(VerifyEmail).get_html_ja(
                email_verify_token, user.account_name, os.getenv("SUPPORT_URL")
            )
        bk.add_task(
            get_di_class(Mailer).send, subject=convert_lang("auth.email.subject"), to=[user.email], body=template
        )
        return user

    # サインイン
    async def sign_in(self, email: str, password: str) -> dict:
        # emailとpasswordが一致するユーザーを取得
        user = await authenticate_user(email, password)
        if not isinstance(user, Users):
            raise HTTPException(status_code=403, detail=convert_lang("auth.error.incorrect_email_or_password"))
        # アクセストークン作成
        claim = crate_user_claim(user)
        token = create_access_token(claim)
        # リフレッシュトークンの有効期限作成
        refresh_token = create_refresh_token()
        expires_at = create_expire_at()
        user = await self.repository.active_update(user.id, refresh_token, expires_at)
        return {"token": token, "refresh_token": refresh_token}

    # サインアウト
    async def sign_out(self, user: Users) -> bool:
        user = await self.repository.inactive_update(user)
        if user is None:
            return False
        return True

    # リフレッシュトークンユーザー認証
    async def get_refresh_token(self, token: str) -> SignUpUser:
        user = await self.repository.get_user_by_refresh_token(token)
        if user is None:
            raise HTTPException(status_code=403, detail=convert_lang("auth.error.invalid_refresh_token"))
        if not user.is_active:
            raise HTTPException(status_code=400, detail=convert_lang("auth.error.inactive_user"))
        if user.deleted_at is not None:
            raise HTTPException(status_code=400, detail=convert_lang("auth.error.deleted_user"))
        # アクセストークン作成
        claim = crate_user_claim(user)
        token = create_access_token(claim)
        # リフレッシュトークンの有効期限作成
        refresh_token = create_refresh_token()
        expires_at = create_expire_at()
        user = await self.repository.active_update(user.id, refresh_token, expires_at)  # type: ignore
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
        if ev.email_verified_expired_at is not None:
            ev.email_verified_expired_at = ev.email_verified_expired_at.replace(tzinfo=timezone.utc)
        if ev is None:
            raise HTTPException(status_code=400, detail=convert_lang("common_error.not_found"))
        if ev.email_verified_expired_at is None or ev.email_verified_expired_at < datetime.now(timezone.utc):
            raise HTTPException(status_code=400, detail=convert_lang("common_error.expired_token"))
        user = await self.repository.get_user_by_id(ev.user_id)
        if user is None:
            raise HTTPException(status_code=400, detail=convert_lang("common_error.not_found_user"))
        if user.email_verified:
            raise HTTPException(status_code=400, detail=convert_lang("auth.error.alradey_verified"))
        # 認証保存処理
        await self.repository.email_verify_update(user, ev)

        return {"result": True, "detail": convert_lang("auth.email_verified")}
