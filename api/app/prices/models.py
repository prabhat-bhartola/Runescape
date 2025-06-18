import ulid
from app.common.models import RunescapeBaseModel
from app.database.core import Base
from sqlmodel import Field, Relationship


class Price(Base, RunescapeBaseModel, table=True):
    id: str = Field(
        default_factory=lambda: str(ulid.new()),
        primary_key=True,
        nullable=False,
    )  # Putting id as ulid as it resembles more to item id

    high: int
    high_time: int
    low: int
    low_time: int

    item_id: str = Field(foreign_key="item.id", unique=True, index=True)
    item: "Item" = Relationship()
