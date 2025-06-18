from typing import Dict, List

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from .models import Price


async def get_all(async_db_session: AsyncSession) -> List[Price]:
    """
    Fetch all prices from the database.
    """
    stmt = select(Price)
    result = await async_db_session.exec(stmt)
    return result.all()


async def bulk_update(
    async_db_session: AsyncSession, *, prices_list: List[Dict]
) -> None:
    await async_db_session.bulk_update_mappings(Price, prices_list)
