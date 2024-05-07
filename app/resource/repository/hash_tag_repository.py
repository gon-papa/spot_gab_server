import logging
from typing import List
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select

from app.db.db import DatabaseConnection
from app.resource.depends.depends import get_di_class
from app.resource.model.hash_tags import HashTags

logger = logging.getLogger("app.exception")


class HashTagRepository:
    def __init__(self) -> None:
        self.db = get_di_class(DatabaseConnection)

    async def findHashTag(self, hashTags: List[str]) -> List[HashTags]:
        async with self.db.get_db() as session:
            try:
                statement = (
                    select(HashTags)
                    .where(HashTags.tag.in_(hashTags))
                )
                result = await session.exec(statement)
                existing_hashtags = [item[0] for item in result.all()]
                # tag属性のみのsetを作成
                existing_tags_set = {hashtag.tag for hashtag in existing_hashtags}
                # 重複していないtagを取得(新たなtag)
                non_existing_tags = [tag for tag in hashTags if tag not in existing_tags_set]

                if non_existing_tags:
                    # タグオブジェクトを作成
                    new_hashtags = [HashTags(tag=tag) for tag in non_existing_tags]
                    session.add_all(new_hashtags)
                    await session.commit()
                    for hashtag in new_hashtags:
                        await session.refresh(hashtag)
                    existing_hashtags.extend(new_hashtags)

                return existing_hashtags
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
