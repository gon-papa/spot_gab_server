from sqlalchemy import Column, String, Date, DateTime, Integer, Boolean, text, func
from sqlalchemy_utils import UUIDType
from app.db.db import Base
from uuid import uuid4

class User(Base):
    id: int
    uuid: str
    account_name: str
    id_account: str
    email: str
    hashed_password: str
    is_active: bool
    birth_date: Date
    other_user_invitation_code: str
    deleted_at: Date
    created_at: DateTime
    updated_at: DateTime
    
    __tablename__ = "users"
    __table_args__ = {"comment": "ユーザー情報テーブル"}

    id = Column(
        Integer,
        primary_key=True,
    )
    uuid = Column(
        UUIDType(binary=False),
        primary_key=True,
        default=uuid4,
        unique=True,
        nullable=False,
        comment="ID",
    )
    account_name = Column(String(length=100), nullable=False, comment="アカウント名")
    id_account = Column(String(length=100), nullable=False, unique=True, comment="アカウントID")
    email = Column(String(length=100), nullable=False, unique=True, comment="メールアドレス")
    hashed_password = Column(String(length=100), nullable=False, comment="パスワード")
    is_active = Column(Boolean, default=True, comment="アクティブフラグ True:ログイン中 False:ログアウト中")
    birth_date = Column(Date, nullable=False, comment="生年月日")
    other_user_invitation_code = Column(UUIDType(binary=False), nullable=True, comment="他ユーザー招待コード")
    deleted_at = Column(Date, nullable=True, comment="削除日時とフラグ")
    created_at = Column(DateTime, default=func.now(), nullable=False, comment="作成日時")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False, comment="更新日時")


