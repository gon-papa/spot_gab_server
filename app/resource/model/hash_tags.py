
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import Column
from sqlmodel import Field, Relationship, SQLModel, Integer, String, TIMESTAMP

from app.resource.model.hash_tag_posts import HashTagPosts


class HashTags(SQLModel, table=True):
    __tablename__ = "hash_tags"
    id: Optional[int] = Field(default=None, sa_column=Column(Integer, primary_key=True, comment="ID"))
    tag: str = Field(sa_column=Column(String(100), nullable=False, unique=True, comment="ハッシュタグ"))
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
    posts: List["Posts"] = Relationship(back_populates="hash_tags", link_model=HashTagPosts)  # type: ignore  # noqa: F821 E501
    hash_tag_posts: List["HashTagPosts"] = Relationship(back_populates="hash_tag")  # type: ignore  # noqa: F821 E501