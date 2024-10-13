from pydantic import BaseModel


class Stock(BaseModel):
    name: str
    quantity: int
