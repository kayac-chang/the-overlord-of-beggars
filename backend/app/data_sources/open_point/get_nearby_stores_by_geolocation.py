import aiohttp
from pydantic import BaseModel, Field

from app.models.geolocation import GeoLocation

from .model import Response
from .share import USER_AGENT


class CategoryStockItem(BaseModel):
    node_id: int = Field(alias="NodeID", description="商品分類編號")
    name: str = Field(alias="Name", description="商品分類名稱")
    remaining_qty: int = Field(
        alias="RemainingQty", description="該商品分類的剩餘即期品數量"
    )


class StoreStockItem(BaseModel):
    store_no: str = Field(alias="StoreNo", description="門市編號")
    store_name: str = Field(alias="StoreName", description="門市名稱")
    distance: float = Field(alias="Distance", description="與用戶的距離")
    is_operate_time: bool = Field(alias="IsOperateTime", description="是否正在營運時間")
    remaining_qty: int = Field(alias="RemainingQty", description="剩餘即期品總數量")
    category_stock_items: list[CategoryStockItem] = Field(
        alias="CategoryStockItems", description="商品分類清單"
    )


class NearbyStoreDetailResponse(BaseModel):
    store_stock_item_list: list[StoreStockItem] = Field(
        alias="StoreStockItemList", description="即期品相關資訊列表"
    )

    store_item_stock_update_time: str = Field(
        alias="StoreItemStockUpdateTime", description="門市即期品更新時間"
    )


async def get_nearby_stores_by_geolocation(
    token: str, current_location: GeoLocation, search_location: GeoLocation
) -> NearbyStoreDetailResponse:
    """
    get nearby stores by geolocation 取得鄰近門市庫存清單 (從經緯度)

    POST /Search/FrontendStoreItemStock/GetNearbyStoreList?token=$token
    user-agent: $user_agent
    content-type: application/json
    """

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"https://lovefood.openpoint.com.tw/LoveFood/api/Search/FrontendStoreItemStock/GetNearbyStoreList",
            params={"token": token},
            headers={"user-agent": USER_AGENT},
            json={
                "CurrentLocation": {
                    "Latitude": current_location["latitude"],
                    "Longitude": current_location["longitude"],
                },
                "SearchLocation": {
                    "Latitude": search_location["latitude"],
                    "Longitude": search_location["longitude"],
                },
            },
        ) as response:

            response_json = await response.json()

            res = Response[NearbyStoreDetailResponse].model_validate(response_json)

            return res.element
