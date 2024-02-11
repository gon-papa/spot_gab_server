from datetime import date, datetime
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
    deleted_at: Optional[date] = Field(sa_column=Column(Date, nullable=True, comment="削除日時とフラグ"))
    created_at: datetime = Field(default_factory=datetime.now, sa_column=Column(DateTime, nullable=True, default=datetime.now))
    updated_at: datetime = Field(default_factory=datetime.now, sa_column=Column(DateTime, nullable=True, onupdate=datetime.now))