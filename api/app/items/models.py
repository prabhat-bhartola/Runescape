import random

from app.common.models import RunescapeBaseModel
from app.database.core import Base
from sqlmodel import Field


class Item(Base, RunescapeBaseModel, table=True):
    id: str = Field(
        default_factory=lambda: str(random.randint(1000, 9999))
    )  # Putting id as random string for simplicity
    name: str
    examine: str
    limit: int
    members: bool
    lowalch: int
    value: int
    highalch: int
    icon: str
