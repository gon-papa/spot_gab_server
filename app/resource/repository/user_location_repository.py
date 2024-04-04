
from app.db.db import DatabaseConnection
from app.resource.depends.depends import get_di_class
from app.resource.model.user_locations import UserLocations
from sqlalchemy.exc import SQLAlchemyError


class UserLocationRepository:
    def __init__(self) -> None:
        self.db = get_di_class(DatabaseConnection)

    async def save_location(self, location: UserLocations) -> UserLocations:
        async with self.db.get_db() as session:
            try:
                session.add(location)
                await session.commit()
                await session.refresh(location)
                return location
            except SQLAlchemyError as e:
                session.rollback()
                raise e
