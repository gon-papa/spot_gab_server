from datetime import date, datetime, timedelta
from typing import Optional
from uuid import uuid4
from sqlmodel import SQLModel, Field, Date, DateTime, Column, Integer, String, Boolean, func, UUID

class Users(SQLModel, table=True):
    id: Optional[int] = Field(default=None, sa_column=Column(Integer, primary_key=True, comment="ID"))
    uuid: str = Field(default_factory=lambda: str(uuid4()), sa_column=Column(String(36), nullable=False, unique=True, comment="UUID"))
    account_name: str = Field(sa_column=Column(String(100), nullable=False, comment="アカウント名"))
    id_account: str = Field(sa_column=Column(String(100), nullable=False, unique=True, comment="アカウントID"))
    email: str = Field(sa_column=Column(String(100), nullable=False, unique=True, comment="メールアドレス"))
    hashed_password: str = Field(sa_column=Column(String(100), nullable=False, comment="パスワード"))
    is_active: bool = Field(sa_column=Column(Boolean, nullable=False, comment="アクティブフラグ True:ログイン中 False:ログアウト中"))
    birth_date: date = Field(sa_column=Column(Date, nullable=False, comment="生年月日"))
    other_user_invitation_code: str = Field(default_factory=lambda: str(uuid4()), sa_column=Column(String(36), nullable=True, comment="他ユーザー招待コード"))
    refresh_token: str = Field(sa_column=Column(String(100), nullable=True, comment="リフレッシュトークン"))
    expires_at: datetime = Field(sa_column=Column(DateTime, nullable=True, comment="リフレッシュトークン有効期限"))
    deleted_at: Optional[datetime] = Field(sa_column=Column(DateTime, nullable=True, comment="削除日時とフラグ"))
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime, nullable=True, default=datetime.utcnow))
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime, nullable=True, onupdate=datetime.utcnow))
    
class UserRead(SQLModel):
    id: int
    uuid: str
    account_name: str
    id_account: str
    email: str
    is_active: bool
    birth_date: date
    other_user_invitation_code: Optional[str] = None
    deleted_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    class ConfigDict:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "uuid": "string",
                "account_name": "string",
                "id_account": "string",
                "email": "string",
                "is_active": True,
                "birth_date": "2021-01-01",
                "other_user_invitation_code": "string",
                "deleted_at": "2021-01-01T00:00:00",
                "created_at": "2021-01-01T00:00:00",
                "updated_at": "2021-01-01T00:00:00"
            }
        }
        
class SignUpUser(SQLModel):
    id: int
    uuid: str
    account_name: str
    id_account: str
    email: str
    birth_date: date
    other_user_invitation_code: Optional[str] = None
    token: Optional[str] = None
    refresh_token: str
    expires_at: datetime
    deleted_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    class ConfigDict:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "uuid": "string",
                "account_name": "string",
                "id_account": "string",
                "email": "string",
                "birth_date": "2021-01-01",
                "other_user_invitation_code": "string",
                "token": "string",
                "refresh_token": "string",
                "expires_at": "2021-01-01T00:00:00",
                "deleted_at": "2021-01-01T00:00:00",
                "created_at": "2021-01-01T00:00:00",
                "updated_at": "2021-01-01T00:00:00"
            }
        }