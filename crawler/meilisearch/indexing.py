import meilisearch
import psycopg
from config import settings


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
                (store_id, store_name, _, address, _, _) = row

                stores.append(
                    {
                        "store_id": store_id,
                        "store_name": store_name,
                        "address": address,
                        # "brand": brand,
                        # "longitude": longitude,
                        # "latitude": latitude,
                    }
                )

            await conn.commit()

    # ===============================

    print("將商店資料寫入 MeiliSearch...")

    client = meilisearch.Client(settings.MEILISEARCH_URL, settings.MEILI_MASTER_KEY)

    task = client.delete_index("stores")
    client.wait_for_task(task.task_uid)

    task = client.create_index("stores", {"primaryKey": "store_id"})
    client.wait_for_task(task.task_uid)

    task = client.index("stores").add_documents(stores)
    client.wait_for_task(task.task_uid)

    print("腳本完成")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
