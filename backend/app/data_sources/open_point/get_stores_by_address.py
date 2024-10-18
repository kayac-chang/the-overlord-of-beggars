import aiohttp

from .model import Response, Store
from .share import USER_AGENT


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
