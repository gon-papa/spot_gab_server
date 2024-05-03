from sqlalchemy.exc import SQLAlchemyError

from app.db.db import DatabaseConnection
from app.resource.depends.depends import get_di_class
from app.resource.model.posts import Posts


class PostRepository:
    def __init__(self) -> None:
        self.db = get_di_class(DatabaseConnection)

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
