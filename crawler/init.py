import psycopg
from config import settings
from sql import init_sql


async def main():
    print("初始化 / 檢查 資料庫...")

    async with await psycopg.AsyncConnection.connect(settings.DATABASE_URL) as conn:
        async with conn.cursor() as cur:
            await cur.execute(init_sql)
            await conn.commit()

    print("腳本完成")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
