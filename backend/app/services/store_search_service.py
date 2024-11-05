import psycopg
from openai import AsyncClient

from app.models.brand import Brand
from app.models.geolocation import GeoLocation
from app.models.store import Store


class StoreSearchService:
    def __init__(self, openai_api_key: str, db_url: str):
        self.client = AsyncClient(api_key=openai_api_key)
        self.db_url = db_url

    async def get_stores_by_keyword_and_location(
        self, keyword: str, location: GeoLocation, brands: set[Brand] | None
    ) -> list[Store]:
        # generate embedding from keyword
        res = await self.client.embeddings.create(
            input=keyword, model="text-embedding-3-small", dimensions=1536
        )
        embedding = str(res.data[0].embedding)

        # do similarity search with the embedding
        search_distance = 1000
        limit = 50
        stores = []

        async with await psycopg.AsyncConnection.connect(self.db_url) as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    """
                    SELECT
                        s.store_id,
                        s.store_name,
                        s.brand,
                        s.address,
                        ST_X(s.coordinates::geometry) as latitude,
                        ST_Y(s.coordinates::geometry) as longitude,
                        ST_Distance(s.coordinates, ST_MakePoint(%(longitude)s, %(latitude)s)) as distance,
                        e.embedding <=> %(embedding)s as cosine_similarity
                    FROM
                        stores_embeddings e
                    JOIN
                        stores s
                    ON
                        e.store_id = s.store_id AND e.brand = s.brand
                    WHERE
                        s.brand = ANY(%(brands)s)
                    AND
                        ST_DWithin(s.coordinates, ST_MakePoint(%(longitude)s, %(latitude)s), %(search_distance)s)
                    ORDER BY
                        cosine_similarity
                    LIMIT
                        %(limit)s
                    """,
                    {
                        "embedding": embedding,
                        "brands": list(brands or ["7-11", "FamilyMart"]),
                        "longitude": location["longitude"],
                        "latitude": location["latitude"],
                        "search_distance": search_distance,
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
                        distance,
                        _,
                    ) = record

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
        # generate embedding from keyword
        res = await self.client.embeddings.create(
            input=keyword, model="text-embedding-3-small", dimensions=1536
        )
        embedding = str(res.data[0].embedding)

        # do similarity search with the embedding
        limit = 50
        stores = []

        async with await psycopg.AsyncConnection.connect(self.db_url) as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    """
                    SELECT
                        s.store_id,
                        s.store_name,
                        s.brand,
                        s.address,
                        ST_X(s.coordinates::geometry) as latitude,
                        ST_Y(s.coordinates::geometry) as longitude,
                        e.embedding <=> %(embedding)s as cosine_similarity
                    FROM
                        stores_embeddings e
                    JOIN
                        stores s
                    ON
                        e.store_id = s.store_id AND e.brand = s.brand
                    WHERE
                        s.brand = ANY(%(brands)s)
                    ORDER BY
                        cosine_similarity
                    LIMIT
                        %(limit)s
                    """,
                    {
                        "embedding": embedding,
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
                        _,
                    ) = record

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
