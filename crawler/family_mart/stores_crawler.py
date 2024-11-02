import aiohttp
import psycopg
from config import settings
from list_of_city import list_of_city
from sql import init_sql, upsert_stores
from tqdm import tqdm

from .get_stores_by_city_and_town import Store, get_stores_by_city_and_town
from .get_towns_by_city import Town, get_towns_by_city


async def main():
    key = settings.FAMILY_MART_KEY

    async with aiohttp.ClientSession() as session:

        print("取得所有城市的行政區...")

        towns: list[Town] = []
        for i in tqdm(range(0, len(list_of_city))):
            city = list_of_city[i]

            towns += await get_towns_by_city(
                session=session, key=key, city=city["city_name"]
            )

        # =================================================

        print("取得所有行政區的門市...")

        stores: list[Store] = []
        for i in tqdm(range(0, len(towns))):
            town = towns[i]

            stores += await get_stores_by_city_and_town(
                session=session, key=key, city=town.city_name, town=town.town_name
            )

        # =================================================

        print("寫入資料庫...")

        async with await psycopg.AsyncConnection.connect(settings.DATABASE_URL) as conn:
            async with conn.cursor() as cur:
                await cur.executemany(
                    upsert_stores,
                    [store.model_dump() | {"brand": "FamilyMart"} for store in stores],
                )
                await conn.commit()

        print("腳本完成")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
