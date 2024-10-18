from pydantic import BaseModel


class Stock(BaseModel):
    name: str
    quantity: int
    category_id: str
    category_name: str
