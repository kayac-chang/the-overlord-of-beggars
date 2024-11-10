import psycopg
from meilisearch_python_sdk import AsyncClient

from app.models.brand import Brand
from app.models.geolocation import GeoLocation
from app.models.store import Store


class StoreSearchService:
    def __init__(
        self, db_url: str, search_engine_url: str, search_engine_master_key: str
    ):
        self.db_url = db_url
        self.search_engine_url = search_engine_url
        self.search_engine_master_key = search_engine_master_key

    async def get_stores_by_keyword_and_location(
        self, keyword: str, location: GeoLocation, brands: set[Brand] | None
    ) -> list[Store]:
        async with AsyncClient(
            self.search_engine_url, self.search_engine_master_key
        ) as client:
            res = await client.index("stores").search(
                keyword,
                show_ranking_score=True,
                limit=50,
                ranking_score_threshold=0.9,
            )

        stores: list[Store] = []
        async with await psycopg.AsyncConnection.connect(self.db_url) as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    """
                    SELECT
                        store_id,
                        store_name,
                        brand,
                        address,
                        ST_X(coordinates::geometry) AS longitude,
                        ST_Y(coordinates::geometry) AS latitude,
                        ST_Distance(coordinates, ST_MakePoint(%(longitude)s, %(latitude)s)) as distance
                    FROM
                        stores
                    WHERE
                        brand = ANY(%(brands)s)
                    AND
                        store_id = ANY(%(store_ids)s)
                    """,
                    {
                        "brands": list(brands or ["7-11", "FamilyMart"]),
                        "store_ids": [[hit["store_id"] for hit in res.hits]],
                        "longitude": location["longitude"],
                        "latitude": location["latitude"],
                    },
                )

                rows = await cur.fetchall()

                for hit in res.hits:
                    store_id = hit["store_id"]

                    # Find the row with the matching store_id, maybe not found
                    row = next((row for row in rows if row[0] == store_id), None)
                    if not row:
                        continue

                    (
                        store_id,
                        store_name,
                        brand,
                        address,
                        longitude,
                        latitude,
                        distance,
                    ) = row
                    stores.append(
                        Store(
                            id=store_id,
                            name=store_name,
                            brand=brand,
                            address=address,
                            latitude=latitude,
                            longitude=longitude,
                            distance=distance,
                        )
                    )

                await conn.commit()
        return stores

    async def get_stores_by_keyword(
        self, keyword: str, brands: set[Brand] | None
    ) -> list[Store]:
        async with AsyncClient(
            self.search_engine_url, self.search_engine_master_key
        ) as client:
            res = await client.index("stores").search(
                keyword,
                show_ranking_score=True,
                limit=50,
                ranking_score_threshold=0.9,
            )

        stores: list[Store] = []
        async with await psycopg.AsyncConnection.connect(self.db_url) as conn:
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
                    WHERE
                        brand = ANY(%(brands)s)
                    AND
                        store_id = ANY(%(store_ids)s)
                    """,
                    {
                        "brands": list(brands or ["7-11", "FamilyMart"]),
                        "store_ids": [[hit["store_id"] for hit in res.hits]],
                    },
                )

                rows = await cur.fetchall()

                for hit in res.hits:
                    store_id = hit["store_id"]

                    # Find the row with the matching store_id, maybe not found
                    row = next((row for row in rows if row[0] == store_id), None)
                    if not row:
                        continue

                    (store_id, store_name, brand, address, longitude, latitude) = row
                    stores.append(
                        Store(
                            id=store_id,
                            name=store_name,
                            brand=brand,
                            address=address,
                            latitude=latitude,
                            longitude=longitude,
                        )
                    )

                await conn.commit()

        return stores

    async def get_stores_by_location(
        self, location: GeoLocation, brands: set[Brand] | None
    ) -> list[Store]:

        search_distance = 1000
        limit = 50
        stores = []

        async with await psycopg.AsyncConnection.connect(self.db_url) as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    """
                    SELECT
                        store_id,
                        store_name,
                        brand,
                        address,
                        ST_X(coordinates::geometry) as latitude,
                        ST_Y(coordinates::geometry) as longitude,
                        ST_Distance(coordinates, ST_MakePoint(%(longitude)s, %(latitude)s)) as distance
                    FROM
                        stores
                    WHERE
                        brand = ANY(%(brands)s)
                    AND
                        ST_DWithin(coordinates, ST_MakePoint(%(longitude)s, %(latitude)s), %(search_distance)s)
                    ORDER BY
                        distance
                    LIMIT
                        %(limit)s
                    """,
                    {
                        "longitude": location["longitude"],
                        "latitude": location["latitude"],
                        "search_distance": search_distance,
                        "brands": list(brands or ["7-11", "FamilyMart"]),
                        "limit": limit,
                    },
                )

                async for record in cur:
                    (
                        store_id,
                        store_name,
                        brand,
                        address,
                        latitude,
                        longitude,
                        search_distance,
                    ) = record

                    stores.append(
                        Store(
                            id=store_id,
                            name=store_name,
                            brand=brand,
                            address=address,
                            latitude=latitude,
                            longitude=longitude,
                            distance=search_distance,
                        )
                    )

                await conn.commit()

        return stores

    async def get_store_by_store_id(self, id: str, brand: Brand) -> Store | None:

        store = None

        async with await psycopg.AsyncConnection.connect(self.db_url) as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    """
                    SELECT
                        store_id,
                        store_name,
                        brand,
                        address,
                        ST_X(coordinates::geometry) as latitude,
                        ST_Y(coordinates::geometry) as longitude
                    FROM
                        stores
                    WHERE
                        store_id = %(store_id)s
                    AND
                        brand = %(brand)s
                    """,
                    {"store_id": id, "brand": brand},
                )

                record = await cur.fetchone()

                if record:
                    (store_id, store_name, brand, address, latitude, longitude) = record

                    store = Store(
                        id=store_id,
                        name=store_name,
                        brand=brand,
                        address=address,
                        latitude=latitude,
                        longitude=longitude,
                    )

                await conn.commit()

        return store

    async def get_store_by_store_id_and_location(
        self, id: str, location: GeoLocation, brand: Brand
    ) -> Store | None:

        store = None

        async with await psycopg.AsyncConnection.connect(self.db_url) as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    """
                    SELECT
                        store_id,
                        store_name,
                        brand,
                        address,
                        ST_X(coordinates::geometry) as latitude,
                        ST_Y(coordinates::geometry) as longitude,
                        ST_Distance(coordinates, ST_MakePoint(%(longitude)s, %(latitude)s)) as distance
                    FROM
                        stores
                    WHERE
                        store_id = %(store_id)s
                    AND
                        brand = %(brand)s
                    ORDER BY
                        distance
                    """,
                    {
                        "store_id": id,
                        "brand": brand,
                        "longitude": location["longitude"],
                        "latitude": location["latitude"],
                    },
                )

                record = await cur.fetchone()

                if record:
                    (
                        store_id,
                        store_name,
                        brand,
                        address,
                        latitude,
                        longitude,
                        distance,
                    ) = record

                    store = Store(
                        id=store_id,
                        name=store_name,
                        brand=brand,
                        address=address,
                        latitude=latitude,
                        longitude=longitude,
                        distance=distance,
                    )

                await conn.commit()

        return store
