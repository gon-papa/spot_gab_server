from typing import List
from app.db.db import DatabaseConnection
from app.resource.depends.depends import get_di_class
from app.resource.model.files import Files
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select


class FileRepository:
    def __init__(self) -> None:
        self.db = get_di_class(DatabaseConnection)

    async def create(self, files: List[Files]) -> Files:
        async with self.db.get_db() as session:
            try:
                session.add_all(files)
                await session.commit()
                for file in files:
                    await session.refresh(file)
                return files
            except SQLAlchemyError as e:
                session.rollback()
                raise e

    async def findByUuid(self, uuid: str) -> Files:
        async with self.db.get_db() as session:
            try:
                result = await session.exec(
                    select(Files).where(
                        Files.uuid == uuid
                    )
                )
                return result.scalar_one_or_none()
            except SQLAlchemyError as e:
                raise e
