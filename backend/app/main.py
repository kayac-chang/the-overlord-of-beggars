from typing import Annotated

from fastapi import FastAPI, Path, Query, Request
from geopy import distance
from pydantic import TypeAdapter

from .config import settings
from .data_sources.open_point.get_access_token import get_access_token
from .data_sources.open_point.get_store_detail import get_store_detail
from .data_sources.open_point.get_stores_by_address import get_stores_by_address
from .data_sources.open_point.get_stores_by_geolocation import get_stores_by_geolocation
from .models.geolocation import GeoLocation
from .models.response import Response
from .models.stock import Stock
from .models.store import Store

app = FastAPI()


def parse_list(param_name: str):
    def parse(request: Request):
        return request.query_params[param_name].split(",")

    return parse


@app.get("/stores")
async def get_stores(
    location: Annotated[
        str | None,
        Query(description="經緯度座標", regex=r"^-?\d+\.\d+,-?\d+\.\d+$"),
    ] = None,
    keyword: Annotated[str | None, Query(description="關鍵字")] = None,
) -> Response[list[Store]]:
    """
    查詢門市
    """
    # @todo: refactor the code

    if keyword:
        # get access token for open point
        token = await get_access_token(settings.OPEN_POINT_MID_V)

        # search the stores from data sources ( 7-11, FamilyMart, ...etc )
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

            # if user location is provided,
            # calculate the distance between the store and the user
            if location:
                [latitude, longitude] = location.split(",")

                # parse the location to GeoLocation
                loc = TypeAdapter(GeoLocation).validate_python(
                    {"latitude": latitude, "longitude": longitude}
                )
                store.distance = distance.distance(
                    (_store.latitude, _store.longitude),
                    (loc["latitude"], loc["longitude"]),
                ).m

            # append the store information to the list
            stores.append(store)

        # if user location is provided,
        # sort the stores by distance
        if location:

            def sort_by_distance(store: Store):
                assert store.distance is not None
                return store.distance

            stores.sort(key=sort_by_distance)

        # sort by the keyword matches
        else:

            # how many characters are matched between the query address and the store address
            def get_keyword_matches(store: Store):
                return len(set(keyword) & set(store.address))

            stores.sort(key=get_keyword_matches, reverse=True)

        return Response(data=stores)

    if location:
        [latitude, longitude] = location.split(",")

        # parse the location to GeoLocation
        loc = TypeAdapter(GeoLocation).validate_python(
            {"latitude": latitude, "longitude": longitude}
        )

        # get access token for open point
        token = await get_access_token(settings.OPEN_POINT_MID_V)

        # search the stores from data sources by geolocation
        _stores = await get_stores_by_geolocation(
            token=token,
            current_location=loc,
            search_location=loc,
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
                    distance=_store.distance,
                )
            )

        # sort the stores by distance
        def sort_by_distance(store: Store):
            assert store.distance is not None
            return store.distance

        stores.sort(key=sort_by_distance)

        return Response(data=stores)

    raise ValueError

    # @todo: background. save the stores to the database


@app.get("/stores/{store_id}/stock")
async def get_store_stock(store_id: str = Path()) -> Response[list[Stock]]:
    """
    查詢門市庫存
    """

    # get access token for open point
    token = await get_access_token(settings.OPEN_POINT_MID_V)

    # search the stock of the stores from data sources
    detail = await get_store_detail(token=token, store_id=store_id)

    stocks = []
    for category_stock_item in detail.store_stock_item.category_stock_items:
        for item in category_stock_item.items:
            stocks.append(
                Stock(
                    name=item.item_name,
                    quantity=item.remaining_qty,
                    category_id=str(category_stock_item.node_id),
                    category_name=category_stock_item.name,
                )
            )

    # @todo: background. save the stock information to the database

    return Response(data=stocks)
