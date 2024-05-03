
from datetime import timezone, datetime
from typing import TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Column, Integer, ForeignKey, TIMESTAMP, Relationship

if TYPE_CHECKING:
    from app.resource.model.hash_tags import HashTags
    from app.resource.model.posts import Posts


class HashTagPosts(SQLModel, table=True):
    __tablename__ = "hash_tag_posts"
    id: Optional[int] = Field(default=None, sa_column=Column(Integer, primary_key=True, comment="ID"))
    post_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey('posts.id'),
            nullable=False,
            comment="ユーザーID",
        )
    )
    hash_tag_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey('hash_tags.id'),
            nullable=False,
            comment="ハッシュタグID",
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
    post: "Posts" = Relationship(back_populates="hash_tag_posts")
    hash_tag: "HashTags" = Relationship(back_populates="hash_tag_posts")
