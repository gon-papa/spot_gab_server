import logging
from typing import List
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import desc
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload

from app.db.db import DatabaseConnection
from app.resource.depends.depends import get_di_class
from app.resource.model.locations import Locations
from app.resource.model.posts import Posts

logger = logging.getLogger("app.exception")


class PostRepository:
    def __init__(self) -> None:
        self.db = get_di_class(DatabaseConnection)

    async def getPostList(self, geo_hash: str, keyword: str, page: int, size: int) -> List[Posts]:
        async with self.db.get_db() as session:
            try:
                statement = (
                    select(Posts)
                    .options(
                        joinedload(Posts.location),
                        joinedload(Posts.user),
                        selectinload(Posts.images),
                    )
                    .where(Posts.location.has(Locations.geo_hash.startswith(geo_hash)))
                )
                # keywordが指定されている場合は検索条件に追加
                if keyword is not None and keyword != "":
                    statement = statement.where(Posts.body.contains(keyword))

                # 最新順に取得
                statement = statement.order_by(desc(Posts.created_at))
                # ページング
                statement = statement.offset((page - 1) * size).limit(size)
                result = await session.exec(statement)
                return result.scalars().all()
            except SQLAlchemyError as e:
                session.rollback()
                raise e

    async def createPost(self, post: Posts) -> Posts:
        async with self.db.get_db() as session:
            try:
                session.add(post)
                await session.commit()
                await session.refresh(post)
                return post
            except SQLAlchemyError as e:
                session.rollback()
                raise e
