from typing import List

from geopy import distance

from app.data_sources.open_point.get_access_token import get_access_token
from app.data_sources.open_point.get_store_by_store_id import get_store_by_store_id
from app.data_sources.open_point.get_stores_by_address import get_stores_by_address
from app.data_sources.open_point.get_stores_by_geolocation import (
    get_stores_by_geolocation,
)
from app.models.geolocation import GeoLocation
from app.models.store import Store
from app.services.store_search_service import StoreSearchService


class OpenPointStoreSearchService(StoreSearchService):
    def __init__(self, mid_v: str):
        self.mid_v = mid_v

    async def get_stores_by_keyword_and_location(
        self, keyword: str, location: GeoLocation
    ) -> List[Store]:
        """
        if user location is provided, calculate the distance between the store and the user
        """

        # get access token for open point
        token = await get_access_token(self.mid_v)

        # search the stores from data sources
        _stores = await get_stores_by_address(token=token, keyword=keyword)

        stores: list[Store] = []
        for _store in _stores:
            # filter the stores that are not open, out of stock, or not in operation time
            if _store.is_x_store or not _store.is_operate_time or not _store.has_stock:
                continue

            store = Store(
                id=_store.store_no,
                name=_store.store_name,
                address=_store.address,
                latitude=_store.latitude,
                longitude=_store.longitude,
                distance=distance.distance(
                    (_store.latitude, _store.longitude),
                    (location["latitude"], location["longitude"]),
                ).m,
            )

            # append the store information to the list
            stores.append(store)

        return stores

    async def get_stores_by_keyword(self, keyword: str) -> List[Store]:
        # get access token for open point
        token = await get_access_token(self.mid_v)

        # search the stores from data sources
        _stores = await get_stores_by_address(token=token, keyword=keyword)

        stores: list[Store] = []
        for _store in _stores:
            # filter the stores that are not open, out of stock, or not in operation time
            if _store.is_x_store or not _store.is_operate_time or not _store.has_stock:
                continue

            store = Store(
                id=_store.store_no,
                name=_store.store_name,
                address=_store.address,
                latitude=_store.latitude,
                longitude=_store.longitude,
            )

            # append the store information to the list
            stores.append(store)

        return stores

    async def get_stores_by_location(self, location: GeoLocation) -> List[Store]:
        # get access token for open point
        token = await get_access_token(self.mid_v)

        # search the stores from data sources by geolocation
        _stores = await get_stores_by_geolocation(
            token=token,
            current_location=location,
            search_location=location,
        )

        stores: list[Store] = []
        for _store in _stores:
            # filter the stores that are not open, out of stock, or not in operation time
            if _store.is_x_store or not _store.is_operate_time or not _store.has_stock:
                continue

            # append the store information to the list
            stores.append(
                Store(
                    id=_store.store_no,
                    name=_store.store_name,
                    address=_store.address,
                    latitude=_store.latitude,
                    longitude=_store.longitude,
                    distance=distance.distance(
                        (_store.latitude, _store.longitude),
                        (location["latitude"], location["longitude"]),
                    ).m,
                )
            )

        return stores

    async def get_store_by_store_id(self, id: str) -> Store | None:
        # get the store by store id from data sources
        _store = await get_store_by_store_id(id)

        # if the store is not found, return None
        if _store is None:
            return None

        return Store(
            id=_store.poi_id,
            name=_store.poi_name,
            address=_store.address,
            latitude=_store.latitude,
            longitude=_store.longitude,
        )

    async def get_store_by_store_id_and_location(
        self, id: str, location: GeoLocation
    ) -> Store | None:
        # get the store by store id from data sources
        _store = await self.get_store_by_store_id(id)

        # if the store is not found, return None
        if _store is None:
            return None

        # clone one to avoid changing the original store
        store = Store.model_validate(_store)

        # calculate the distance between the store and the user
        store.distance = distance.distance(
            (store.latitude, store.longitude),
            (location["latitude"], location["longitude"]),
        ).m

        return store
