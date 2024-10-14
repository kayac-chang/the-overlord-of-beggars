from typing import Annotated

from fastapi import FastAPI, Query, Request
from geopy import distance
from pydantic import TypeAdapter

from backend.config import settings
from backend.data_sources.open_point.get_access_token import get_access_token
from backend.data_sources.open_point.get_store_detail import get_store_detail
from backend.data_sources.open_point.get_stores_by_address import get_stores_by_address
from backend.data_sources.open_point.get_stores_by_geolocation import (
    get_stores_by_geolocation,
)
from backend.models.geolocation import GeoLocation
from backend.models.response import Response
from backend.models.stock import Stock
from backend.models.store import Store

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
    address: Annotated[str | None, Query(description="地址")] = None,
) -> Response[list[Store]]:
    """
    查詢門市
    """
    # @todo: refactor the code

    if address:
        # get access token for open point
        token = await get_access_token(settings.OPEN_POINT_MID_V)

        # search the stores from data sources ( 7-11, FamilyMart, ...etc )
        _stores = await get_stores_by_address(token=token, keyword=address)

        stores = []
        for store in _stores:
            # filter the stores that are not open, out of stock, or not in operation time
            if store.is_x_store or not store.is_operate_time or not store.has_stock:
                continue

            # if user location is provided,
            # calculate the distance between the store and the user
            if location:
                [latitude, longitude] = location.split(",")

                # parse the location to GeoLocation
                loc = TypeAdapter(GeoLocation).validate_python(
                    {"latitude": latitude, "longitude": longitude}
                )
                store.distance = distance.distance(
                    (store.latitude, store.longitude),
                    (loc["latitude"], loc["longitude"]),
                ).m

            # append the store information to the list
            stores.append(
                Store(
                    id=store.store_no,
                    name=store.store_name,
                    address=store.address,
                    latitude=store.latitude,
                    longitude=store.longitude,
                    distance=store.distance,
                )
            )

        # if user location is provided,
        # sort the stores by distance
        if location:
            stores.sort(key=lambda store: store.distance)

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

        stores = []
        for store in _stores:
            # filter the stores that are not open, out of stock, or not in operation time
            if store.is_x_store or not store.is_operate_time or not store.has_stock:
                continue

            # append the store information to the list
            stores.append(
                Store(
                    id=store.store_no,
                    name=store.store_name,
                    address=store.address,
                    latitude=store.latitude,
                    longitude=store.longitude,
                    distance=store.distance,
                )
            )

        # sort the stores by distance
        stores.sort(key=lambda store: store.distance)

        return Response(data=stores)

    raise ValueError

    # @todo: background. save the stores to the database


@app.get("/stores/{store_id}/stock")
async def get_store_stock(store_id: str) -> Response[list[Stock]]:
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
                )
            )

    # @todo: background. save the stock information to the database

    return Response(data=stocks)
