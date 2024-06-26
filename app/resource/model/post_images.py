
from datetime import timezone, datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Column, Integer, String, ForeignKey, TIMESTAMP, Relationship

from app.resource.model.posts import Posts


class PostImages(SQLModel, table=True):
    __tablename__ = "post_images"
    id: Optional[int] = Field(default=None, sa_column=Column(Integer, primary_key=True, comment="ID"))
    post_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey('posts.id'),
            nullable=False,
            comment="ユーザーID",
        )
    )
    image_path: Optional[str] = Field(sa_column=Column(String(1024), nullable=True, comment="画像パス"))
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
    post: Optional[Posts] = Relationship(back_populates="images")


class ShowPostImage(SQLModel):
    image_path: str
    created_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "image_path": "https://example.com/image.jpg",
                "created_at": "2021-01-01T00:00:00+00:00"
            }
        }
