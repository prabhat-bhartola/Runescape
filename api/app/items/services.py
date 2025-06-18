from typing import List

from app.common.enums import SortByType
from sqlmodel import select

from .models import Item
from .schemas import ItemSearchQueryParams


async def get_many(
    async_db_session: ItemSearchQueryParams,
    *,
    query_params: ItemSearchQueryParams,
) -> List[Item]:
    stmt = select(Item).where(Item.is_active == True)

    if query_params.name_like is not None:
        stmt = stmt.where(Item.name.like("%{}%".format(query_params.name_like)))

    stmt = stmt.offset(query_params.skip).limit(query_params.limit)

    if query_params.sort_by == SortByType.ASC:
        stmt = stmt.order_by(Item.created_at.asc())
    else:
        stmt = stmt.order_by(Item.created_at.desc())

    result = await async_db_session.exec(stmt)
    return result.all()
