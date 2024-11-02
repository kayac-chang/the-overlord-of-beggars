import aiohttp
import xmltodict

from .models import Response, Store


async def get_stores_by_city_and_town(
    session: aiohttp.ClientSession, city: str, town: str
) -> list[Store] | Store | None:
    """
    get stores by city and town 透過行政區取得門市資訊
    """
    async with session.get(
        f"https://emap.pcsc.com.tw/EMapSDK.aspx",
        params={"commandid": "SearchStore", "city": city, "town": town},
    ) as response:

        response_xml_str = await response.text()

        response_dict = xmltodict.parse(response_xml_str)

        if not "GeoPosition" in response_dict["iMapSDKOutput"]:
            return None

        return Response[list[Store] | Store](
            **response_dict["iMapSDKOutput"]
        ).GeoPosition
