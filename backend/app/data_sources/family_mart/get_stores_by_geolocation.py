import aiohttp
from app.models.geolocation import GeoLocation
from asyncache import cached
from cachetools import LRUCache

from .model import Response, Store
from .share import PROJECT_CODE


def geolocation_to_str(geolocation: GeoLocation) -> str:
    return f"{geolocation['latitude']},{geolocation['longitude']}"


def key_func(current_location: GeoLocation):
    return f"family-{geolocation_to_str(current_location)}"


@cached(cache=LRUCache(maxsize=128), key=key_func)
async def get_stores_by_geolocation(
    current_location: GeoLocation
) -> list[Store]:
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
                "longitude": current_location["longitude"]
            },
        ) as response:

            response_json = await response.json()

            res = Response[list[Store]].model_validate(response_json)

            return res.data

# python -m app.data_sources.family_mart.get_stores_by_geolocation
if __name__ == '__main__':
    import asyncio
    from pydantic import TypeAdapter
    from pprint import pprint


    async def main():
        loc = TypeAdapter(GeoLocation).validate_python(
            {"latitude": 25.035, "longitude": 121.5576 }
        )
        stores = await get_stores_by_geolocation(loc)
        pprint(stores)

    asyncio.run(main())
