from dotenv import load_dotenv
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os

load_dotenv()

dialect = os.getenv("DB_DIALECT")
driver = os.getenv("DB_DRIVER")
username = os.getenv("DB_USER")
password = os.getenv("DB_PASS")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
pool_size = int(os.getenv("DB_POOL_SIZE"))
pool_connection_timeout = int(os.getenv("POOL_CONN_TIMEOUT"))
pool_recycle = int(os.getenv("POOL_RECYCLE"))
max_overflow = int(os.getenv("DB_MAX_OVERFLOW"))
logging = bool(os.getenv("SQL_LOGGING"))

ASYNC_DB_URL = f"{dialect}+{driver}://{username}:{password}@{host}:{port}/{db_name}?charset=utf8"

async_engine = create_async_engine(
    ASYNC_DB_URL,
    echo=logging,
    echo_pool=logging,
    pool_size=pool_size,
    pool_timeout=pool_connection_timeout,
    max_overflow=pool_size,
    pool_recycle=pool_recycle,
    pool_pre_ping=True,
)

AsyncSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession, expire_on_commit=True,
)

Base = declarative_base()

@asynccontextmanager
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session