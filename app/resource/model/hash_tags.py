
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import Column
from sqlmodel import Field, SQLModel, Integer, String, TIMESTAMP


class HashTags(SQLModel, table=True):
    __tablename__ = "hash_tags"
    id: Optional[int] = Field(default=None, sa_column=Column(Integer, primary_key=True, comment="ID"))
    tag: str = Field(sa_column=Column(String(100), nullable=False, comment="ハッシュタグ"))
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
