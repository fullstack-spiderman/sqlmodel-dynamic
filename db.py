# import os
from pprint import pprint
from sqlmodel import SQLModel

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from settings import DBSettings, get_db_settings, AppSettings, get_app_settings

# DATABASE_URI = os.environ.get(
#     "DATABASE_URI", "postgresql+asyncpg://postgres:postgres@localhost:5432/webdev"
# )

# DATABASE_URI = "postgresql+asyncpg://postgres:postgres@localhost:5432/webdev"

# settings = DBSettings(pg_dsn=DATABASE_URI)
# DB_URI = settings.pg_dsn

# print({"DB_URI": DB_URI})

config = get_db_settings()
DATABASE_URI = config.dict()
app_settings = get_app_settings()
# DATABASE_URI = "postgresql+asyncpg://postgres:postgres@localhost:5432/webdev"
pprint(
    {
        'pg_dsn': DATABASE_URI, 'type': type(
            DATABASE_URI), "app_settings": app_settings.environment
    }
)
engine = create_async_engine(
    # DATABASE_URI,
    "postgresql+asyncpg://postgres:postgres@localhost:5432/webdev",
    echo=True, future=True
)


async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all())
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        yield session
