from typing import Generic, TypeVar

import aiohttp
import xmltodict
from pydantic import BaseModel, Field, field_validator

T = TypeVar("T")


class Response(BaseModel, Generic[T]):
    MessageID: str
    CommandID: str
    Status: str
    TimeStamp: str
    GeoPosition: T | None


class Town(BaseModel):
    town_id: str = Field(alias="TownID", description="行政區編號")
    town_name: str = Field(alias="TownName", description="行政區名稱")
    longitude: float = Field(alias="X", description="經度")
    latitude: float = Field(alias="Y", description="緯度")

    @field_validator("longitude", "latitude")
    @classmethod
    def convert_to_float(cls, v: int) -> float:
        return v / 1_000_000


async def get_towns_by_city_id(city_id: str) -> list[Town] | None:
    """
    get town by city id 透過城市編號取得行政區

    POST https://emap.pcsc.com.tw/EMapSDK.aspx
    content-type: application/x-www-form-urlencoded; charset=utf-8
    """

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"https://emap.pcsc.com.tw/EMapSDK.aspx",
            data={"commandid": "GetTown", "cityid": city_id},
        ) as response:
            response_xml_str = await response.text()
            response_dict = xmltodict.parse(response_xml_str)

            if not "GeoPosition" in response_dict["iMapSDKOutput"]:
                return None

            return Response[list[Town]](**response_dict["iMapSDKOutput"]).GeoPosition


async def get_stores_by_city_and_town(city: str, town: str):
    """
    get stores by city and town 透過行政區取得門市資訊

    POST https://emap.pcsc.com.tw/EMapSDK.aspx
    content-type: application/x-www-form-urlencoded; charset=utf-8
    """

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"https://emap.pcsc.com.tw/EMapSDK.aspx",
            data={"commandid": "SearchStore", "city": city, "town": town},
        ) as response:
            response_xml_str = await response.text()
            response_dict = xmltodict.parse(response_xml_str)
            return response_dict


list_of_city = [
    {"city_id": "01", "city_name": "台北市"},
    {"city_id": "02", "city_name": "基隆市"},
    {"city_id": "03", "city_name": "新北市"},
    {"city_id": "04", "city_name": "桃園市"},
    {"city_id": "05", "city_name": "新竹市"},
    {"city_id": "06", "city_name": "新竹縣"},
    {"city_id": "07", "city_name": "苗栗縣"},
    {"city_id": "08", "city_name": "台中市"},
    {"city_id": "10", "city_name": "彰化縣"},
    {"city_id": "11", "city_name": "南投縣"},
    {"city_id": "12", "city_name": "雲林縣"},
    {"city_id": "13", "city_name": "嘉義市"},
    {"city_id": "14", "city_name": "嘉義縣"},
    {"city_id": "15", "city_name": "台南市"},
    {"city_id": "17", "city_name": "高雄市"},
    {"city_id": "19", "city_name": "屏東縣"},
    {"city_id": "20", "city_name": "宜蘭縣"},
    {"city_id": "21", "city_name": "花蓮縣"},
    {"city_id": "22", "city_name": "台東縣"},
    {"city_id": "23", "city_name": "澎湖縣"},
    {"city_id": "24", "city_name": "連江縣"},
    {"city_id": "25", "city_name": "金門縣"},
]


if __name__ == "__main__":
    import asyncio

    async def main():
        # batch request to get all towns by city id, 5 requests concurrently
        tasks = [get_towns_by_city_id(city["city_id"]) for city in list_of_city]

        results = []
        for i in range(0, len(tasks), 5):
            results += await asyncio.gather(*tasks[i : i + 5])
