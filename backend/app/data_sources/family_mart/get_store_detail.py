import aiohttp

from .model import Response, Store
from .share import PROJECT_CODE


async def get_store_detail(store_id: str) -> Store | None:
    """
    get store detail 取得門市庫存

    POST https://stamp.family.com.tw/api/maps/MapProductInfo
    """

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"https://stamp.family.com.tw/api/maps/MapProductInfo",
            json={
                "ProjectCode": PROJECT_CODE,
                "OldPKeys": [store_id],
            },
        ) as response:

            response_json = await response.json()

            return Response[list[Store]].model_validate(response_json).data[0]
