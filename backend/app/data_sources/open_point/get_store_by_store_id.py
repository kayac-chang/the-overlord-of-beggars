import aiohttp
import xmltodict
from pydantic import BaseModel, Field, field_validator


class GeoPosition(BaseModel):
    poi_id: str = Field(alias="POIID", description="店號")
    poi_name: str = Field(alias="POIName", description="店名")
    longitude: float = Field(alias="X", description="經度")
    latitude: int = Field(alias="Y", description="緯度")
    address: str = Field(alias="Address", description="地址")

    @field_validator("longitude", mode="after")
    @classmethod
    def convert_to_longitude(cls, v: int) -> float:
        return v / 1_000_000

    @field_validator("latitude", mode="after")
    @classmethod
    def convert_to_latitude(cls, v: int) -> float:
        return v / 1_000_000


class Response(BaseModel):
    MessageID: str
    CommandID: str
    Status: str
    TimeStamp: str
    GeoPosition: GeoPosition | None


async def get_store_by_store_id(id: str) -> GeoPosition | None:
    """
    get store by store id 透過門市號碼取得門市資訊

    POST https://emap.pcsc.com.tw/EMapSDK.aspx
    content-type: application/x-www-form-urlencoded; charset=utf-8
    """

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"https://emap.pcsc.com.tw/EMapSDK.aspx",
            data={"commandid": "SearchStore", "ID": id},
        ) as response:

            response_xml_str = await response.text()

            response_dict = xmltodict.parse(response_xml_str)

            if not "GeoPosition" in response_dict["iMapSDKOutput"]:
                return None

            return Response(**response_dict["iMapSDKOutput"]).GeoPosition
