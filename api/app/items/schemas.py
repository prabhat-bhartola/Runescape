from typing import Optional

from app.common.schemas import RunescapeBaseSchema, SortPaginateQuery
from pydantic import BaseModel


class ItemSearchQueryParams(SortPaginateQuery):
    name_like: Optional[str] = None


class ItemBaseSchema(BaseModel):
    id: str
    name: str
    examine: str
    limit: int
    members: bool
    lowalch: int
    value: int
    highalch: int
    icon: str


class ItemRead(RunescapeBaseSchema, ItemBaseSchema):
    ...


class ItemCreate(ItemBaseSchema):
    ...
