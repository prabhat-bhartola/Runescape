import random
from typing import Optional

from app.common.models import RunescapeBaseModel
from app.database.core import Base
from sqlmodel import Field, Relationship


class Item(Base, RunescapeBaseModel, table=True):
    id: str = Field(
        default_factory=lambda: str(random.randint(1000, 9999)),
        primary_key=True,
        nullable=False,
    )  # Putting id as random string for simplicity

    name: str = Field(index=True, nullable=False)
    icon: str
    examine: str
    limit: Optional[int] = Field(nullable=True)
    members: bool
    lowalch: Optional[int] = Field(nullable=True)
    value: int = Field(index=True)
    highalch: Optional[int] = Field(nullable=True)

    price: Optional["Price"] = Relationship(back_populates="item")
