from typing import Generic, TypeVar

from pydantic import BaseModel, Field, field_validator

T = TypeVar("T")


class Response(BaseModel, Generic[T]):
    MessageID: str
    CommandID: str
    Status: str
    TimeStamp: str
    GeoPosition: T | None


class Town(BaseModel):
    town_id: str = Field(validation_alias="TownID", description="行政區編號")
    town_name: str = Field(validation_alias="TownName", description="行政區名稱")
    longitude: float = Field(validation_alias="X", description="經度")
    latitude: float = Field(validation_alias="Y", description="緯度")

    @field_validator("longitude", "latitude")
    @classmethod
    def convert_to_float(cls, v: int) -> float:
        return v / 1_000_000


class Store(BaseModel):
    store_id: str = Field(validation_alias="POIID", description="店號")
    store_name: str = Field(validation_alias="POIName", description="店名")
    longitude: float = Field(validation_alias="X", description="經度")
    latitude: float = Field(validation_alias="Y", description="緯度")
    address: str = Field(validation_alias="Address", description="地址")

    @field_validator("longitude", "latitude")
    @classmethod
    def convert_to_float(cls, v: int) -> float:
        return v / 1_000_000
