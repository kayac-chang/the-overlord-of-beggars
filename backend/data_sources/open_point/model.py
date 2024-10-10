from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


# general response model from open point
class Response(BaseModel, Generic[T]):
    element: T
    message: str | None
    is_success: bool = Field(validation_alias="isSuccess")
