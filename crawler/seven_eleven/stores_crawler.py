import aiohttp
import psycopg
from config import settings
from list_of_city import list_of_city
from sql import upsert_stores
from tqdm import tqdm
from utils import flatten

from .get_stores_by_city_and_town import get_stores_by_city_and_town
from .get_towns_by_city_id import get_towns_by_city_id


async def main():
    async with aiohttp.ClientSession() as session:

        print("取得所有城市的行政區...")

        async def fn1(city):
            towns = await get_towns_by_city_id(session, city["city_id"])

            if not towns:
                return []

            return [city | town.model_dump() for town in towns]

        towns = []
        for i in tqdm(range(0, len(list_of_city))):
            towns += await fn1(list_of_city[i])

        towns = list(flatten(towns))

        # =================================================

        print("取得所有行政區的門市...")

        async def fn2(town):
            stores = await get_stores_by_city_and_town(
                session, city=town["city_name"], town=town["town_name"]
            )

            if not stores:
                return []

            if not isinstance(stores, list):
                return [town | stores.model_dump()]

            return [town | store.model_dump() for store in stores]

        stores = []
        for i in tqdm(range(0, len(towns))):
            stores += await fn2(towns[i])

        stores = list(flatten(stores))

        # =================================================

        print("寫入資料庫...")

        async with await psycopg.AsyncConnection.connect(settings.DATABASE_URL) as conn:
            async with conn.cursor() as cur:
                await cur.executemany(
                    upsert_stores, [store | {"brand": "7-11"} for store in stores]
                )
                await conn.commit()

        print("腳本完成")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
