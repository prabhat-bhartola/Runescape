import random
from datetime import datetime

import pytz
from sqlalchemy import event
from sqlmodel import DateTime, Field, SQLModel


class SwarmBaseModel(SQLModel):
    id: str = Field(
        default_factory=lambda: str(random.randint(1000, 9999))
    )  # Putting id as random string for simplicity

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
