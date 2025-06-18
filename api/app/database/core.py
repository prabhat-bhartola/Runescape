import re
from typing import AsyncGenerator

from app.config import settings
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, declarative_base, declared_attr
from sqlmodel.ext.asyncio.session import AsyncSession

async_engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL, echo=True, future=True
)

async_session: AsyncSession = async_sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)


def resolve_table_name(name):
    """Resolves table names to their mapped names."""
    names = re.split("(?=[A-Z])", name)  # noqa
    return "_".join([x.lower() for x in names if x])


class CustomBase:
    @declared_attr
    def __tablename__(self):
        return resolve_table_name(self.__name__)


Base: DeclarativeBase = declarative_base(cls=CustomBase)


def get_class_by_tablename(tablename: str):
    for mapper in Base.registry.mappers:
        if mapper.mapped_table.name == tablename:
            return mapper.class_

    raise ValueError(
        f"Model not found for table name: {tablename}. Check the name of your model."
    )


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
