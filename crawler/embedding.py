import json

import psycopg
from openai import AsyncClient
from pgvector.psycopg import register_vector_async
from tqdm import tqdm

from config import settings
from sql import upsert_stores_embeddings


async def main():
    print("從資料庫取得所有商店...")

    stores: list[dict] = []
    async with await psycopg.AsyncConnection.connect(settings.DATABASE_URL) as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                SELECT
                    store_id,
                    store_name,
                    brand,
                    address,
                    ST_X(coordinates::geometry) AS longitude,
                    ST_Y(coordinates::geometry) AS latitude
                FROM
                    stores
            """
            )

            async for row in cur:
                (store_id, store_name, brand, address, longitude, latitude) = row

                stores.append(
                    {
                        "store_id": store_id,
                        "store_name": store_name,
                        "brand": brand,
                        "address": address,
                        "longitude": longitude,
                        "latitude": latitude,
                    }
                )

            await conn.commit()

    # ===============================

    print("準備用於 embedding 的資料...")

    for store in stores:
        store["raw_embedding"] = json.dumps(store, ensure_ascii=False).replace(" ", "")

    # ===============================

    print("透過 OpenAI 產生商店資訊的 embedding...")

    client = AsyncClient(api_key=settings.OPENAI_API_KEY)
    raw_embeddings = [store["raw_embedding"] for store in stores]
    batch_size = 1000

    for i in tqdm(range(0, len(raw_embeddings), batch_size)):
        res = await client.embeddings.create(
            input=raw_embeddings[i : i + batch_size],
            model="text-embedding-3-small",
            dimensions=512,
        )
        for row in res.data:
            stores[i + row.index]["embedding"] = row.embedding

    # ===============================

    print("將商店 embedding 資料寫入資料庫...")

    async with await psycopg.AsyncConnection.connect(settings.DATABASE_URL) as conn:
        await register_vector_async(conn)

        async with conn.cursor() as cur:
            await cur.executemany(upsert_stores_embeddings, stores)

            await conn.commit()

    print("腳本完成")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
