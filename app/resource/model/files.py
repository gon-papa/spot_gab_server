
from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4
from sqlmodel import SQLModel, Column, Integer, Field, String, TIMESTAMP, Boolean


class Files(SQLModel, table=True):
    __tablename__ = "files"
    id: Optional[int] = Field(default=None, sa_column=Column(Integer, primary_key=True, comment="ID"))
    uuid: str = Field(
        default_factory=lambda: str(uuid4()), sa_column=Column(String(36), nullable=False, unique=True, comment="UUID")
    )
    name: str = Field(sa_column=Column(String(100), nullable=False, comment="ファイル名"))
    path: str = Field(sa_column=Column(String(1024), nullable=False, comment="ファイルパス"))
    is_used: bool = Field(sa_column=Column(Boolean, nullable=False, default=True, comment="使用中フラグ False:未使用 True:使用中"))
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