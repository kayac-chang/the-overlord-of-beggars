from typing import Generic, TypedDict, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


# general response model from open point
class Response(BaseModel, Generic[T]):
    element: T
    message: str | None
    is_success: bool = Field(validation_alias="isSuccess")


class Store(BaseModel):
    store_no: str = Field(alias="StoreNo", description="門市編號")
    store_name: str = Field(alias="StoreName", description="門市名稱")
    store_short_name: str = Field(alias="StoreShortName", description="門市名稱")
    is_enabled: bool = Field(alias="IsEnabled", description="?")
    latitude: float = Field(alias="Latitude", description="門市緯度")
    longitude: float = Field(alias="Longitude", description="門市經度")
    address: str = Field(alias="Address", description="門市地址")
    is_x_store: bool = Field(alias="IsXStore", description="? 關店")
    is_operate_time: bool = Field(alias="IsOperateTime", description="是否正在營運時間")
    has_stock: bool = Field(alias="HasStock", description="是否有即期品庫存")
    distance: float | None = Field(alias="Distance", description="與用戶的距離")


class Location(TypedDict):
    latitude: float
    longitude: float


class SubItemCategory(BaseModel):
    id: int = Field(alias="ID", description="子類別編號")
    name: str = Field(alias="Name", description="子類別名稱")
    is_enabled: bool = Field(alias="IsEnabled", description="?")
    pcsccategeroy_no: list[str] = Field(
        alias="PCSCCategeroyNo", description="統一超商產品類別"
    )


class ItemCategory(BaseModel):
    id: int = Field(alias="ID", description="商品分類編號")
    name: str = Field(alias="Name", description="商品分類名稱")
    image_url: str = Field(alias="ImageUrl", description="商品分類圖片")
    is_enabled: bool = Field(alias="IsEnabled", description="?")
    children: list[SubItemCategory] = Field(
        alias="Children", description="商品分類子類別"
    )
