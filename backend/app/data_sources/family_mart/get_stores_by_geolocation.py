import aiohttp
from asyncache import cached  # type: ignore
from cachetools import LRUCache

from app.models.geolocation import GeoLocation

from .model import Response, Store
from .share import PROJECT_CODE


def geolocation_to_str(geolocation: GeoLocation) -> str:
    return f"{geolocation['latitude']},{geolocation['longitude']}"


def key_func(current_location: GeoLocation):
    return f"family-{geolocation_to_str(current_location)}"


@cached(cache=LRUCache(maxsize=128), key=key_func)
async def get_stores_by_geolocation(current_location: GeoLocation) -> list[Store]:
    """
    get stores by geolocation 取得門市清單 (從經緯度)

    POST https://stamp.family.com.tw/api/maps/MapProductInfo
    """

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"https://stamp.family.com.tw/api/maps/MapProductInfo",
            json={
                "ProjectCode": PROJECT_CODE,
                "latitude": current_location["latitude"],
                "longitude": current_location["longitude"],
            },
        ) as response:

            response_json = await response.json()

            res = Response[list[Store]].model_validate(response_json)

            return res.data
