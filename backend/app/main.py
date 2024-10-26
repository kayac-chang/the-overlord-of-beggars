import sys
from typing import Annotated

from fastapi import FastAPI, Query
from fastapi.exceptions import HTTPException
from pydantic import TypeAdapter

from .config import settings
from .data_sources import family_mart
from .data_sources.open_point.get_access_token import get_access_token
from .data_sources.open_point.get_store_detail import get_store_detail
from .models.geolocation import GeoLocation
from .models.response import Response
from .models.stock import Stock
from .models.store import Store
from .services.family_mart_store_search_service import FamilyMartStoreSearchService
from .services.open_point_store_search_service import OpenPointStoreSearchService
from .services.store_search_reducer import reducer
from .services.store_search_service import StoreSearchService

app = FastAPI()

# add your store search services here
store_search_services: list[StoreSearchService] = [
    OpenPointStoreSearchService(settings.OPEN_POINT_MID_V),
    FamilyMartStoreSearchService(),
]

Location = Annotated[
    str | None,
    Query(description="經緯度座標", regex=r"^-?\d+\.\d+,-?\d+\.\d+$"),
]


@app.get("/stores")
async def get_stores(
    location: Location = None,
    keyword: Annotated[str | None, Query(description="關鍵字")] = None,
) -> Response[list[Store]]:
    """
    查詢門市
    """

    loc = None
    if location:
        [latitude, longitude] = location.split(",")
        loc = TypeAdapter(GeoLocation).validate_python(
            {"latitude": latitude, "longitude": longitude}
        )

    stores = await reducer(store_search_services, keyword, loc)

    return Response(data=stores)

    # @todo: background. save the stores to the database


@app.get("/stores/{store_id}")
async def get_store(
    store_id: str,
    location: Location = None,
) -> Response[Store]:

    loc = None
    if location:
        [latitude, longitude] = location.split(",")
        loc = TypeAdapter(GeoLocation).validate_python(
            {"latitude": latitude, "longitude": longitude}
        )

    # search the store by store id from data sources
    for service in store_search_services:
        if loc:
            store = await service.get_store_by_store_id_and_location(
                id=store_id, location=loc
            )
        else:
            store = await service.get_store_by_store_id(id=store_id)

        if store:
            return Response(data=store)

    raise HTTPException(status_code=404, detail="Item not found")


@app.get("/stores/{store_id}/stock")
async def get_store_stock(store_id: str) -> Response[list[Stock]]:
    """
    查詢門市庫存
    """

    stocks = []

    try:
        # get access token for open point
        token = await get_access_token(settings.OPEN_POINT_MID_V)

        # search the stock of the stores from data sources
        detail = await get_store_detail(token=token, store_id=store_id)

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
    except Exception as e:
        print(e, file=sys.stderr)

    try:
        store = await family_mart.get_store_detail(store_id=store_id)

        if not store:
            raise HTTPException(status_code=404, detail="Item not found")

        for category in store.info:
            for sub_category in category.categories:
                for product in sub_category.products:
                    if not product.qty:
                        continue

                    stocks.append(
                        Stock(
                            name=product.name,
                            quantity=product.qty,
                            category_id=category.code,
                            category_name=category.name,
                        )
                    )

    except Exception as e:
        print(e, file=sys.stderr)

    return Response(data=stocks)

    # @todo: background. save the stock information to the database
