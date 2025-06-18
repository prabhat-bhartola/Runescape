from typing import List

from app.database.core import get_async_session
from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from .schemas import ItemRead, ItemSearchQueryParams
from .services import get_many

router = APIRouter()


@router.get("", response_model=List[ItemRead], summary="Get paginated Items.")
async def get_items(
    query_params: ItemSearchQueryParams = Depends(),
    async_db_session: AsyncSession = Depends(get_async_session),
):
    return await get_many(async_db_session, query_params=query_params)
