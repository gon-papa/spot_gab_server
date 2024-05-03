from datetime import date, datetime, timezone
from typing import List, Optional
from uuid import uuid4

from sqlalchemy import ForeignKey
from sqlmodel import Boolean, Column, Date, Field, Integer, Relationship, SQLModel, String, TIMESTAMP

from app.resource.model.files import Files


class Users(SQLModel, table=True):
    id: Optional[int] = Field(default=None, sa_column=Column(Integer, primary_key=True, comment="ID"))
    image_id: Optional[int] = Field(default=None, sa_column=Column(Integer, ForeignKey('files.id')))
    uuid: str = Field(
        default_factory=lambda: str(uuid4()), sa_column=Column(String(36), nullable=False, unique=True, comment="UUID")
    )
    account_name: str = Field(sa_column=Column(String(100), nullable=False, comment="アカウント名"))
    id_account: str = Field(sa_column=Column(String(100), nullable=False, unique=True, comment="アカウントID"))
    email: str = Field(sa_column=Column(String(100), nullable=False, unique=True, comment="メールアドレス"))
    hashed_password: str = Field(sa_column=Column(String(100), nullable=False, comment="パスワード"))
    is_active: bool = Field(
        sa_column=Column(
            Boolean, nullable=False, default=False, comment="アクティブフラグ True:ログイン中 False:ログアウト中"
        )
    )
    birth_date: date = Field(sa_column=Column(Date, nullable=False, comment="生年月日"))
    other_user_invitation_code: str = Field(
        default_factory=lambda: str(uuid4()),
        sa_column=Column(String(36), nullable=True, comment="他ユーザー招待コード"),
    )
    refresh_token: str = Field(sa_column=Column(String(100), nullable=True, comment="リフレッシュトークン"))
    expires_at: datetime = Field(sa_column=Column(TIMESTAMP(True), nullable=True, comment="リフレッシュトークン有効期限"))
    email_verified: bool = Field(
        sa_column=Column(Boolean, nullable=False, default=False, comment="メール認証フラグ True:認証済 False:未認証")
    )
    profile: Optional[str] = Field(sa_column=Column(String(130), nullable=True, comment="プロフィール"))
    link: Optional[str] = Field(sa_column=Column(String(1024), nullable=True, comment="リンク"))
    deleted_at: Optional[datetime] = Field(sa_column=Column(TIMESTAMP(True), nullable=True, comment="削除日時とフラグ"))
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            TIMESTAMP(True),
            nullable=True,
            default=datetime.now(timezone.utc)
        )
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            TIMESTAMP(True),
            nullable=True,
            onupdate=datetime.now(timezone.utc)
        )
    )
    # リレーション
    email_verifications: Optional["EmailVerification"] = Relationship(back_populates="user")  # type: ignore  # noqa: F821 E501
    file: Optional["Files"] = Relationship(sa_relationship_kwargs={"lazy": "joined"})  # type: ignore  # noqa: F821 E501
    posts: List["Posts"] = Relationship(back_populates="user")  # type: ignore  # noqa: F821 E501


class UserRead(SQLModel):
    id: int
    uuid: str
    image_id: Optional[int] = None
    file: Optional[Files] = None
    account_name: str
    id_account: str
    email: str
    is_active: bool
    birth_date: date
    other_user_invitation_code: Optional[str] = None
    email_verified: bool
    profile: Optional[str] = None
    
    link: Optional[str] = None
    deleted_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class ConfigDict:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "image_id": 1,
                "uuid": "string",
                "file": {
                    "id": 1,
                    "uuid": "string",
                    "name": "string",
                    "path": "string",
                    "is_used": True,
                    "created_at": "2021-01-01T00:00:00",
                    "updated_at": "2021-01-01T00:00:00",
                },
                "account_name": "string",
                "id_account": "string",
                "email": "string",
                "is_active": True,
                "birth_date": "2021-01-01",
                "other_user_invitation_code": "string",
                "email_verified": True,
                "profile": "string",
                "link": "string",
                "deleted_at": "2021-01-01T00:00:00",
                "created_at": "2021-01-01T00:00:00",
                "updated_at": "2021-01-01T00:00:00",
            }
        }


class AuthenticatedUser(SQLModel):
    id: int
    image_id: Optional[int] = None
    uuid: str
    file: Optional[Files] = None
    account_name: str
    id_account: str
    email: str
    birth_date: date
    other_user_invitation_code: str | None = None
    token: str | None = None
    refresh_token: str
    expires_at: datetime
    email_verified: bool
    profile: str | None = None
    link: str | None = None
    deleted_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class ConfigDict:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "image_id": 1,
                "uuid": "string",
                "file": {
                    "id": 1,
                    "uuid": "string",
                    "name": "string",
                    "path": "string",
                    "is_used": True,
                    "created_at": "2021-01-01T00:00:00",
                    "updated_at": "2021-01-01T00:00:00",
                },
                "account_name": "string",
                "id_account": "string",
                "email": "string",
                "birth_date": "2021-01-01",
                "other_user_invitation_code": "string",
                "token": "string",
                "refresh_token": "string",
                "expires_at": "2021-01-01T00:00:00",
                "email_verified": True,
                "profile": "string",
                "link": "string",
                "deleted_at": "2021-01-01T00:00:00",
                "created_at": "2021-01-01T00:00:00",
                "updated_at": "2021-01-01T00:00:00",
            }
        }


class Me(SQLModel):
    id: int
    image_id: Optional[int] = None
    uuid: str
    file: Optional[Files] = None
    account_name: str
    id_account: str
    email: str
    birth_date: date
    other_user_invitation_code: str | None = None
    expires_at: datetime
    email_verified: bool
    profile: str | None = None
    link: str | None = None
    deleted_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class ConfigDict:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "image_id": 1,
                "uuid": "string",
                "file": {
                    "id": 1,
                    "uuid": "string",
                    "name": "string",
                    "path": "string",
                    "is_used": True,
                    "created_at": "2021-01-01T00:00:00",
                    "updated_at": "2021-01-01T00:00:00",
                },
                "account_name": "string",
                "id_account": "string",
                "email": "string",
                "birth_date": "2021-01-01",
                "other_user_invitation_code": "string",
                "expires_at": "2021-01-01T00:00:00",
                "email_verified": True,
                "profile": "string",
                "link": "string",
                "deleted_at": "2021-01-01T00:00:00",
                "created_at": "2021-01-01T00:00:00",
                "updated_at": "2021-01-01T00:00:00",
            }
        }

