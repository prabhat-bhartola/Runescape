from typing import Dict, Optional

from app.common.models import RunescapeBaseModel
from app.database.core import get_class_by_tablename
from asyncpg.exceptions import UniqueViolationError
from sqlalchemy.exc import IntegrityError, InvalidRequestError, ResourceClosedError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from .exceptions import Conflict, UnprocessableEntity


async def get_one_by(
    async_db_session: AsyncSession, *, tablename: str, filters: Dict
) -> Optional[RunescapeBaseModel]:
    db_model: RunescapeBaseModel = get_class_by_tablename(tablename)

    stmt = select(db_model)

    for key, value in filters.items():
        stmt = stmt.where(
            getattr(db_model, key) == value
        )  # ? Will multiple where work?

    result = await async_db_session.exec(stmt)
    return result.first()


async def create(
    async_db_session: AsyncSession,
    *,
    tablename: str,
    data_in: Dict,
) -> RunescapeBaseModel:
    try:
        db_model: RunescapeBaseModel = get_class_by_tablename(tablename)
        row = db_model(**data_in)

        async_db_session.add(row)
        await async_db_session.commit()
        return row
    except IntegrityError as e:
        await async_db_session.rollback()
        if isinstance(e.orig, UniqueViolationError):
            raise Conflict(error_msg=f"{tablename} already exists.")
        else:
            raise
    except (ResourceClosedError, InvalidRequestError):
        await async_db_session.rollback()
        raise UnprocessableEntity


async def get_or_create(
    async_db_session: AsyncSession,
    *,
    tablename: str,
    search_by: Dict,
    create_data: Dict,
) -> RunescapeBaseModel:
    existing_record: Optional[RunescapeBaseModel] = await get_one_by(
        async_db_session, tablename=tablename, filters=search_by
    )
    return existing_record or await create(
        async_db_session, tablename=tablename, data_in=create_data
    )
