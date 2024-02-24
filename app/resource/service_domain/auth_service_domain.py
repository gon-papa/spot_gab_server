from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from jose import JWTError, jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import os
from passlib.context import CryptContext
from pydantic import BaseModel
from app.resource.repository.user_repository import UserRepository
from app.resource.model.users import Users
from typing import Optional, Union
from app.resource.depends.depends import get_di_class

import secrets
import logging

load_dotenv()
logger = logging.getLogger("app.exception")

class TokenData(BaseModel):
    uuid: Union[str, None] = None

class Token(BaseModel):
    access_token: str
    token_type: str
    
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="sign-in")

secret_key = os.getenv('JWT_SECRET_KEY')

algorithm = "HS256"

expired_minutes = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))


# パスワード比較
def verify_password(plain_password, hashed_password)-> bool:
    return pwd_context.verify(plain_password, hashed_password)

# パスワードのハッシュ化
def get_password_hash(password)-> str:
    return pwd_context.hash(password)

# リフレッシュトークン作成
def create_refresh_token()-> str:
    return secrets.token_urlsafe(64)

# リフレッシュトークンの有効期限作成
def create_expire_at()-> datetime:
    day = int(os.getenv('REFRESH_TOKEN_EXPIRE_DAY'))
    create_expire_at = datetime.utcnow() + timedelta(days=day)
    return create_expire_at

# 認証チェック
# emailとpasswordが一致するユーザーを取得
async def authenticate_user(email: str, password: str)-> Union[Users, bool]:
    repository = get_di_class(UserRepository)
    user = await repository.get_user_by_email(email)
    if user is None:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# jwtペイロード作成
def crate_user_claim(user: Users)-> dict:
    access_token_data = {
        "sub": user.uuid, # 一意の識別子
        "aud": "user", # role
        "exp": datetime.utcnow() + timedelta(minutes=expired_minutes), # 有効期限
    }
    return access_token_data

# アクセストークン作成
def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt

# アクセストークン解析
async def get_current_user(token: str = Depends(oauth2_scheme))-> Optional[Users]:
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm], audience="user")
        uuid: str = payload.get("sub")
        if uuid is None:
            credentials_exception(None)
    except JWTError as e:
        credentials_exception(e)
    user = await get_di_class(UserRepository).get_user_by_uuid(uuid)
    if user is None:
        credentials_exception(None)
    return user

# 解析失敗時の例外
def credentials_exception(e: Union[JWTError, None]):
    logger.error(e)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

# ユーザー認証
async def get_current_active_user(current_user: Users = Depends(get_current_user))-> Users:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    if current_user.deleted_at is not None:
        raise HTTPException(status_code=400, detail="Deleted user")
    return current_user