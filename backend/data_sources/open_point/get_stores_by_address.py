import aiohttp
from pydantic import BaseModel, Field

from .model import Response
from .share import USER_AGENT


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


async def get_stores_by_address(token: str, keyword: str) -> list[Store]:
    """
    get stores by address 取得門市清單 (從店名/地址)

    POST /Master/FrontendStore/GetStoreByAddress?token=$token&keyword=$url_encode_keyword
    user-agent: $user_agent
    """

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"https://lovefood.openpoint.com.tw/LoveFood/api/Master/FrontendStore/GetStoreByAddress",
            params={"token": token, "keyword": keyword},
            headers={"user-agent": USER_AGENT},
        ) as response:

            response_json = await response.json()

            res = Response[list[Store]].model_validate(response_json)

            return res.element
