from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import ForeignKey
from sqlmodel import (Column, Field, Integer, Relationship, SQLModel, TIMESTAMP, String)

from app.resource.model.users import Users


class EmailVerification(SQLModel, table=True):
    __tablename__ = "email_verifications"
    id: Optional[int] = Field(default=None, sa_column=Column(Integer, primary_key=True, comment="ID"))
    user_id: int = Field(
        default=None,
        sa_column=Column(
            Integer,
            ForeignKey("users.id"),
            nullable=False,
            unique=True,
            comment="ユーザーID"
        )
    )
    email_verified_at: Optional[datetime] = Field(sa_column=Column(TIMESTAMP(True), nullable=True, comment="メール認証日時"))
    email_verify_token: str = Field(sa_column=Column(String(100), nullable=True, comment="メール認証トークン"))
    email_verified_expired_at: Optional[datetime] = Field(
        sa_column=Column(
            TIMESTAMP(True),
            nullable=True,
            comment="メール認証有効期限"
        )
    )
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
    user: Optional[Users] = Relationship(back_populates="email_verifications")
