import aiohttp
import xmltodict

from models import Response, Town


async def get_towns_by_city_id(
    session: aiohttp.ClientSession, city_id: str
) -> list[Town] | None:
    """
    get town by city id 透過城市編號取得行政區
    """
    async with session.get(
        f"https://emap.pcsc.com.tw/EMapSDK.aspx",
        params={"commandid": "GetTown", "cityid": city_id},
    ) as response:

        response_xml_str = await response.text()

        response_dict = xmltodict.parse(response_xml_str)

        if not "GeoPosition" in response_dict["iMapSDKOutput"]:
            return None

        return Response[list[Town]](**response_dict["iMapSDKOutput"]).GeoPosition
