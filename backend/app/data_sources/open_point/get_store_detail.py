import aiohttp
from app.models.geolocation import GeoLocation
from pydantic import BaseModel, Field

from .model import Response
from .share import USER_AGENT


class Item(BaseModel):
    item_name: str = Field(alias="ItemName", description="商品名稱")
    remaining_qty: int = Field(alias="RemainingQty", description="商品數量")


class CategoryStockItem(BaseModel):
    node_id: int = Field(alias="NodeID", description="商品分類編號")
    name: str = Field(alias="Name", description="商品分類名稱")
    remaining_qty: int = Field(
        alias="RemainingQty", description="該商品分類的剩餘即期品數量"
    )
    items: list[Item] = Field(alias="ItemList", description="商品清單")


class StoreStockItem(BaseModel):
    store_no: str = Field(alias="StoreNo", description="門市編號")
    store_name: str = Field(alias="StoreName", description="門市名稱")
    distance: float = Field(alias="Distance", description="與用戶的距離")
    is_operate_time: bool = Field(alias="IsOperateTime", description="是否正在營運時間")
    remaining_qty: int = Field(alias="RemainingQty", description="剩餘即期品總數量")
    category_stock_items: list[CategoryStockItem] = Field(
        alias="CategoryStockItems", description="商品分類清單"
    )


class StoreDetailResponse(BaseModel):
    store_stock_item: StoreStockItem = Field(
        alias="StoreStockItem", description="門市庫存清單"
    )
    store_item_stock_update_time: str = Field(
        alias="StoreItemStockUpdateTime", description="門市即期品更新時間"
    )


async def get_store_detail(
    token: str,
    store_id: str,
    current_location: GeoLocation = {"latitude": 0, "longitude": 0},
) -> StoreDetailResponse:
    """
    get store detail 取得門市庫存

    POST /Search/FrontendStoreItemStock/GetStoreDetail?token=$token
    user-agent: $user_agent
    content-type: application/json
    """

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"https://lovefood.openpoint.com.tw/LoveFood/api/Search/FrontendStoreItemStock/GetStoreDetail",
            params={"token": token},
            headers={"user-agent": USER_AGENT},
            json={
                "CurrentLocation": {
                    "Latitude": current_location["latitude"],
                    "Longitude": current_location["longitude"],
                },
                "StoreNo": store_id,
            },
        ) as response:

            response_json = await response.json()

            res = Response[StoreDetailResponse].model_validate(response_json)

            return res.element
