from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel
from app.resource.repository.user_repository import UserRepository
from app.resource.model.users import Users


class Token(BaseModel):
    access_token: str
    token_type: str
    
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")




# パスワード比較
def verify_password(plain_password, hashed_password)-> bool:
    return pwd_context.verify(plain_password, hashed_password)

# パスワードのハッシュ化
def get_password_hash(password)-> str:
    return pwd_context.hash(password)

#user取得
def get_user(user_repository:UserRepository, email: str)-> Users:
    user = user_repository.get_user_by_email(email)
    if user is None:
        return None
    return user