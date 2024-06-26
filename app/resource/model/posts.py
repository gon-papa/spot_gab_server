from datetime import datetime, timezone
from typing import List, Optional
from uuid import uuid4
from sqlalchemy import Column, ForeignKey
from sqlmodel import Field, SQLModel, Integer, String, Text, TIMESTAMP, Relationship
from app.resource.model.hash_tag_posts import HashTagPosts
from app.resource.model.locations import Locations
from app.resource.model.users import Users


class Posts(SQLModel, table=True):
    __tablename__ = "posts"
    id: Optional[int] = Field(default=None, sa_column=Column(Integer, primary_key=True, comment="ID"))
    uuid: str = Field(
        default_factory=lambda: str(uuid4()), sa_column=Column(String(36), nullable=False, unique=True, comment="UUID")
    )
    user_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("users.id"),
            nullable=False,
            comment="ユーザーID",
        )
    )
    location_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("locations.id"),
            nullable=False,
            comment="位置情報ID",
        )
    )
    body: str = Field(sa_column=Column(Text, nullable=False, comment="本文"))
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(TIMESTAMP(True), nullable=True, default=datetime.now(timezone.utc)),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(TIMESTAMP(True), nullable=True, onupdate=datetime.now(timezone.utc)),
    )
    user: Optional[Users] = Relationship(back_populates="posts")
    location: Optional[Locations] = Relationship(back_populates="posts")
    images: List["PostImages"] | None = Relationship(back_populates="post")  # type: ignore  # noqa: F821 E501
    hash_tags: List["HashTags"] = Relationship(back_populates="posts", link_model=HashTagPosts)  # type: ignore  # noqa: F821 E501
    hash_tag_posts: List["HashTagPosts"] = Relationship(back_populates="post")  # type: ignore  # noqa: F821 E501


class ShowPosts(SQLModel):
    uuid: str
    body: str
    created_at: datetime

    class ConfigDict:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "uuid": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                "body": "本文",
                "created_at": "2021-01-01T00:00:00",
            }
        }
