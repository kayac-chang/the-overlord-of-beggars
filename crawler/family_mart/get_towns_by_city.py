import json
import re

import aiohttp
import pydantic


class Town(pydantic.BaseModel):
    post: str = pydantic.Field(validation_alias="post", description="郵遞區號")
    town_name: str = pydantic.Field(validation_alias="town", description="行政區名稱")
    city_name: str = pydantic.Field(validation_alias="city", description="城市名")


async def get_towns_by_city(
    session: aiohttp.ClientSession, key: str, city: str
) -> list[Town]:
    """
    get town by city 透過城市名稱取得行政區
    """
    async with session.get(
        "https://api.map.com.tw/net/familyShop.aspx",
        headers={
            "Referer": "https://www.family.com.tw/",
        },
        params={
            "searchType": "ShowTownList",
            "type": "",
            "fun": "storeTownList",
            "key": key,
            "city": city,
        },
    ) as response:
        response_txt = await response.text()

        response_txt = re.sub(r"\s+", " ", response_txt).strip()
        matches = re.findall(r"\((.*?)\)", response_txt, re.DOTALL)
        response_json = json.loads(matches[0])

        return pydantic.TypeAdapter(list[Town]).validate_python(response_json)
