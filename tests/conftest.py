import asyncio
import logging
import os
import pytest_asyncio
from app.resource.model.users import *
from app.resource.depends.depends import update_injector, get_di_class
from app.db.db import DatabaseConnection, TestAppConfig

@pytest_asyncio.fixture
async def set_up_test():
    print("before")
    db_connection = get_di_class(DatabaseConnection)
    await db_connection.close_engine()
    await update_injector(TestAppConfig())
    db_connection = get_di_class(DatabaseConnection)
    db_connection.get_db()
    engine = db_connection.engine
    async with engine.begin() as conn:
        # SQLModel.metadata.create_all でテーブルを作成
        await conn.run_sync(SQLModel.metadata.create_all)
    
    yield
    print("after")