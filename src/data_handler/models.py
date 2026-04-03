from typing import Annotated

from pydantic import BaseModel, Field


class EquitiesSchema(BaseModel):
    """Represents a single equity with symbol, name and intraday price."""

    symbol: str
    name: str
    price: Annotated[float, Field(gt=0)]
