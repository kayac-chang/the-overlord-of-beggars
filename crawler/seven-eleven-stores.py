import aiohttp

from get_stores_by_city_and_town import get_stores_by_city_and_town
from get_towns_by_city_id import get_towns_by_city_id
from utils import flatten

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


async def main():
    async with aiohttp.ClientSession() as session:

        # 1. 取得所有城市的行政區
        async def fn1(city):
            towns = await get_towns_by_city_id(session, city["city_id"])

            if not towns:
                return []

            return [city | town.model_dump() for town in towns]

        tasks = [fn1(city) for city in list_of_city]

        towns = await asyncio.gather(*tasks)

        towns = list(flatten(towns))

        # 2. 取得所有行政區的7-11門市
        async def fn2(town):
            stores = await get_stores_by_city_and_town(
                session, city=town["city_name"], town=town["town_name"]
            )

            if not stores:
                return []

            if not isinstance(stores, list):
                return [town | stores.model_dump()]

            return [town | store.model_dump() for store in stores]

        tasks = [fn2(town) for town in towns]

        stores = await asyncio.gather(*tasks)

        stores = list(flatten(stores))

        # @todo 寫入資料庫

    pass


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
