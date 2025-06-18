from datetime import datetime

import pytz
from sqlalchemy import event
from sqlmodel import DateTime, Field, SQLModel


class RunescapeBaseModel(SQLModel):
    # id: UUID = Field(
    #     default_factory=uuid4,
    #     primary_key=True,
    #     nullable=False,
    # ) # Skip uuid ids as we need integer ids

    is_active: bool = Field(default=True)

    created_at: datetime = Field(
        sa_type=DateTime(timezone=True), default_factory=lambda: datetime.now(pytz.utc)
    )
    created_at._creation_order = 9998

    updated_at: datetime = Field(
        sa_type=DateTime(timezone=True), default_factory=lambda: datetime.now(pytz.utc)
    )
    updated_at._creation_order = 9998

    @staticmethod
    def _updated_at(mapper, connection, target):
        target.updated_at = datetime.now(pytz.utc)

    @classmethod
    def __declare_last__(cls):
        event.listen(cls, "before_update", cls._updated_at)
