from typing import Literal

from pydantic import BaseModel


class Store(BaseModel):
    id: str
    name: str
    address: str
    latitude: float
    longitude: float
    distance: float | None = None
    brand: Literal["7-11", "FamilyMart"]
