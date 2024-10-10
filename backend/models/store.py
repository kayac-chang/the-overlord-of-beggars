from pydantic import BaseModel


class Store(BaseModel):
    id: int
    name: str
    address: str
    latitude: float
    longitude: float
