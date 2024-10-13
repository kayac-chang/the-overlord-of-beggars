import aiohttp

from .model import ItemCategory, Response
from .share import USER_AGENT


async def get_item_categories(token: str) -> list[ItemCategory]:
    """
    get item categories 取得商品分類

    POST /Master/FrontendItemCategory/GetList?token=$token
    user-agent: $user_agent
    """

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"https://lovefood.openpoint.com.tw/LoveFood/api/Master/FrontendItemCategory/GetList",
            params={"token": token},
            headers={"user-agent": USER_AGENT},
        ) as response:

            response_json = await response.json()

            res = Response[list[ItemCategory]].model_validate(response_json)

            return res.element
