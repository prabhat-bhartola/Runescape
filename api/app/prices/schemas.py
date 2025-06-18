from app.common.schemas import RunescapeBaseSchema
from pydantic import BaseModel


class PriceBaseSchema(BaseModel):
    high: int
    high_time: int
    low: int
    low_time: int


class PriceRead(RunescapeBaseSchema, PriceBaseSchema):
    id: str


class PriceCreate(PriceBaseSchema):
    ...
