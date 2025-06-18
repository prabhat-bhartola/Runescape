from typing import Optional

from app.common.schemas import RunescapeBaseSchema, SortPaginateQuery
from pydantic import BaseModel


class ItemSearchQueryParams(SortPaginateQuery):
    name_like: Optional[str] = None


class ItemBaseSchema(BaseModel):
    id: str
    name: str
    examine: str
    limit: Optional[int]
    members: bool
    lowalch: Optional[int]
    value: int
    highalch: Optional[int]
    icon: str


class ItemRead(RunescapeBaseSchema, ItemBaseSchema):
    ...


class ItemCreate(ItemBaseSchema):
    ...
