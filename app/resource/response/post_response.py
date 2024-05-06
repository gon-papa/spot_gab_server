
from typing import List
from pydantic import BaseModel, Field
from app.resource.model.locations import ShowLocation
from app.resource.model.post_images import ShowPostImage
from app.resource.model.posts import ShowPosts
from app.resource.model.users import UserRead
from app.resource.response.json_response import JsonResponse


class PostResponse(JsonResponse):
    class PostResponseItem(BaseModel):
        post: ShowPosts = Field(None, description="投稿情報")
        postImages: List[ShowPostImage] = Field([], description="画像情報")
        user: UserRead = Field(None, description="ユーザー情報")
        location: ShowLocation = Field(None, description="位置情報")
    data: List[PostResponseItem] = Field(None, description="投稿情報リスト")
