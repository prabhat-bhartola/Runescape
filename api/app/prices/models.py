from typing import Optional

from app.common.models import RunescapeBaseModel
from app.database.core import Base
from sqlmodel import Field, Relationship
from ulid import ULID


class Price(Base, RunescapeBaseModel, table=True):
    id: str = Field(
        default_factory=lambda: str(ULID()),
        primary_key=True,
        nullable=False,
    )  # Putting id as ulid as it resembles more to item id

    high: Optional[int] = Field(nullable=True)
    high_time: Optional[int] = Field(nullable=True)
    low: Optional[int] = Field(nullable=True)
    low_time: Optional[int] = Field(nullable=True)

    item_id: str = Field(foreign_key="item.id", unique=True, index=True)
    item: "Item" = Relationship()
