import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncEngine

from app.db.db import AppConfig, DatabaseConnection, TestAppConfig
from app.resource.depends.depends import get_di_class, update_injector
from sqlmodel import SQLModel


# functionごとに実行される
@pytest_asyncio.fixture(autouse=True, scope='function')
async def set_up_test():
    try:
        engine = await change_db(TestAppConfig())
        async with engine.begin() as conn:
            # SQLModel.metadata.create_all でテーブルを作成
            await conn.run_sync(SQLModel.metadata.create_all)

        yield
    finally:
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.drop_all)
        await change_db(AppConfig())


async def change_db(_class) -> AsyncEngine:
    db_connection = get_di_class(DatabaseConnection)
    await db_connection.close_engine()
    await update_injector(_class)
    db_connection = get_di_class(DatabaseConnection)
    db_connection.get_db()
    return db_connection.engine
