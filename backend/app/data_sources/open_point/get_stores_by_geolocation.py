import aiohttp
from app.models.geolocation import GeoLocation

from .model import Response, Store
from .share import USER_AGENT


async def get_stores_by_geolocation(
    token: str, current_location: GeoLocation, search_location: GeoLocation
) -> list[Store]:
    """
    get stores by geolocation 取得門市清單 (從經緯度)

    POST /Master/FrontendStore/GetStoreListByGeoLocation
    user-agent: $user_agent
    content-type: application/json
    """

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"https://lovefood.openpoint.com.tw/LoveFood/api/Master/FrontendStore/GetStoreListByGeoLocation",
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

            res = Response[list[Store]].model_validate(response_json)

            return res.element
