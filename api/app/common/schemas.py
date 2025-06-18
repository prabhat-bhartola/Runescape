from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from .enums import SortByType

config = ConfigDict(
    from_attributes=True,
    validate_assignment=True,
    arbitrary_types_allowed=True,
    str_strip_whitespace=True,
)


class RunescapeBaseSchema(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = config


class SortPaginateQuery(BaseModel):
    sort_by: Optional[SortByType] = SortByType.ASC
    skip: Optional[int] = Field(default=0)
    limit: Optional[int] = Field(default=50, ge=0, le=100)


class Brief(BaseModel):
    id: UUID
    name: str
