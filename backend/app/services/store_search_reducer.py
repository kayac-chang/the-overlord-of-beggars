from typing import Sequence
import sys

from app.models.geolocation import GeoLocation
from app.models.store import Store

from .store_search_service import StoreSearchService


async def mapper(
    service: StoreSearchService, keyword: str | None, location: GeoLocation | None
) -> list[Store]:
    match (keyword, location):
        case (
            str() as keyword,
            {"latitude": float(), "longitude": float()} as location,
        ):
            return await service.get_stores_by_keyword_and_location(keyword, location)

        case (str() as keyword, None):
            return await service.get_stores_by_keyword(keyword)

        case (None, {"latitude": float(), "longitude": float()} as location):
            return await service.get_stores_by_location(location)
        case _:
            raise ValueError


async def sorter(
    stores: list[Store], keyword: str | None, location: GeoLocation | None
) -> list[Store]:
    # if user keyword is provided, sort the stores by keyword matches
    if keyword:
        # how many characters are matched between the query address and the store address
        def get_keyword_matches(store: Store):
            return len(set(keyword) & set(store.address))

        return sorted(stores, key=get_keyword_matches, reverse=True)

    # if user location is provided, sort the stores by distance
    if location:

        def sort_by_distance(store: Store):
            assert store.distance is not None
            return store.distance

        return sorted(stores, key=sort_by_distance, reverse=False)

    else:
        raise ValueError


async def reducer(
    services: Sequence[StoreSearchService],
    keyword: str | None,
    loc: GeoLocation | None,
):
    stores = []

    # todo: run the map function in parallel (multiprocessing)
    for service in services:
        stores += await mapper(service, keyword, loc)

    stores = await sorter(stores, keyword, loc)

    return stores
