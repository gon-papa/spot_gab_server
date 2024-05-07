from datetime import datetime, timezone
from decimal import Decimal
from fastapi import HTTPException
from typing import List
from xmlrpc.client import boolean
from app.resource.model.hash_tags import HashTags
from app.resource.model.locations import Locations
from injector import inject

from app.resource.model.post_images import PostImages
from app.resource.model.posts import Posts
from app.resource.model.users import Users
from app.resource.repository.hash_tag_repository import HashTagRepository
from app.resource.repository.post_repository import PostRepository
from app.resource.request.post_request import PostRequest


class PostService:
    @inject
    def __init__(
        self,
        repository: PostRepository,
        hashTagRepository: HashTagRepository,
    ):
        self.repository = repository
        self.hashTagRepository = hashTagRepository

    """_summary_
    投稿一覧取得
    Args:
    request : PostRequest
        リクエスト
    user : Users
        ユーザー
    Returns:
        投稿一覧
    """

    async def index(self, request: PostRequest, user: Users) -> List[Posts]:
        try:
            return await self.repository.getPostList(
                geo_hash=request.geo_hash, keyword=request.keyword, page=request.page, size=request.size
            )
        except Exception:
            raise HTTPException(status_code=500, detail="Internal Server Error")

    # 投稿保存
    async def store(self, request: PostRequest, user: Users) -> boolean:
        try:
            location = await self._createLocationObject(
                request.lat,
                request.lng,
                request.point,
                request.geo_hash,
                request.country,
                request.administrative_area,
                request.sub_administrative_area,
                request.locality,
                request.sub_locality,
                request.postal_code,
                request.name,
                request.street,
                request.iso_country_code,
                request.thoroughfare,
                request.sub_thoroughfare,
            )
            posts = await self._createPostObject(request.body)
            post_images = await self._createPostImageObject(request.images)
            # 同一のハッシュタグは保存せずに、既存のものを取得する(この際に前後の空白を削除する)
            tags = await self._createTagObject(request.hashtags)

            # リレーション込みで保存
            posts.location = location
            posts.user = user
            posts.images = post_images
            posts.hash_tags = tags
            result = await self.repository.createPost(posts)
            return result
        except Exception:
            raise HTTPException(status_code=500, detail="Internal Server Error")

    async def _createLocationObject(
        self,
        lat: Decimal,
        lng: Decimal,
        point: str,
        geo_hash: str,
        country: str | None,
        administrative_area: str | None,
        sub_administrative_area: str | None,
        locality: str | None,
        sub_locality: str | None,
        postal_code: str | None,
        name: str | None,
        street: str | None,
        iso_country_code: str | None,
        thoroughfare: str | None,
        sub_thoroughfare: str | None,
    ) -> Locations:
        return Locations(
            lat=lat,
            lng=lng,
            point=point,
            geo_hash=geo_hash,
            srid="4326",
            save_datetime=datetime.now(timezone.utc),
            country=country,
            administrative_area=administrative_area,
            sub_administrative_area=sub_administrative_area,
            locality=locality,
            sub_locality=sub_locality,
            postal_code=postal_code,
            name=name,
            street=street,
            iso_country_code=iso_country_code,
            thoroughfare=thoroughfare,
            sub_thoroughfare=sub_thoroughfare,
        )

    async def _createPostObject(
        self,
        body: str,
    ):
        return Posts(
            body=body,
        )

    async def _createPostImageObject(
        self,
        paths: List[str],
    ) -> List[PostImages]:
        return [
            PostImages(
                image_path=path,
            )
            for path in paths
        ]

    async def _createTagObject(
        self,
        tags: List[str],
    ) -> List[HashTags]:
        if not tags:
            return []
        return await self.hashTagRepository.findHashTag(tags)
