from typing import Generic, TypeVar

from pydantic import BaseModel, Field, computed_field

T = TypeVar("T")


class Response(BaseModel, Generic[T]):
    data: T
    message: str
    code: int = Field()


class ProductWithoutQty(BaseModel):
    code: str = Field(validation_alias="productCode", description="商品編號")
    name: str = Field(validation_alias="productName", description="商品名稱")


class SubItemCategoryWithoutQty(BaseModel):
    code: str = Field(validation_alias="categoryCode", description="商品子分類編號")
    name: str = Field(validation_alias="categoryName", description="商品子分類名稱")
    products: list[ProductWithoutQty] = Field()


class ItemCategoryWithoutQty(BaseModel):
    code: str = Field(validation_alias="groupCode", description="商品分類編號")
    name: str = Field(validation_alias="groupName", description="商品分類名稱")
    icon_url: str = Field(alias="iconURL", description="商品分類圖片")
    categories: list[SubItemCategoryWithoutQty] = Field()

class ProductWithSubCategory(BaseModel):
    code: str = Field(description="商品編號")
    name: str = Field(description="商品名稱")
    qty: int | None = Field(description="商品庫存數量")
    sub_category_code: str = Field(description="商品子分類編號")
    sub_category_name: str = Field(description="商品子分類名稱")

class Product(BaseModel):
    code: str = Field(description="商品編號")
    name: str = Field(description="商品名稱")
    qty: int | None = Field(description="商品庫存數量")


class SubItemCategory(BaseModel):
    code: str = Field(description="商品子分類編號")
    name: str = Field(description="商品子分類名稱")
    qty: int | None = Field(description="商品子分類庫存數量")
    products: list[Product] = Field()


class ItemCategory(BaseModel):
    code: str = Field(description="商品分類編號")
    name: str = Field(description="商品分類名稱")
    icon_url: str = Field(alias="iconURL", description="商品分類圖片")
    qty: int | None = Field(description="商品分類庫存數量")
    categories: list[SubItemCategory] = Field()


class Store(BaseModel):
    store_no: str = Field(validation_alias="oldPKey", description="門市編號")
    store_name: str = Field(validation_alias="name", description="門市名稱")
    latitude: float = Field(validation_alias="latitude", description="門市緯度")
    longitude: float = Field(validation_alias="longitude", description="門市經度")
    address: str = Field(validation_alias="address", description="門市地址")
    distance: float = Field(validation_alias="distance", description="與用戶的距離")
    updated_at: str = Field(validation_alias="updateDate", description="ISO8601, 門市即期品更新時間")
    info: list[ItemCategory] = Field()

    @computed_field
    @property
    def has_stock(self) -> bool:
        for category in self.info:
            if category.qty is not None and category.qty > 0:
                return True
        return False
