from typing import Annotated
import sys

from fastapi import FastAPI, Path, Query, Request
from pydantic import TypeAdapter

from .config import settings
from .data_sources.open_point.get_access_token import get_access_token
from .data_sources.open_point.get_store_detail import get_store_detail
from .data_sources import family_mart
from .models.geolocation import GeoLocation
from .models.response import Response
from .models.stock import Stock
from .models.store import Store
from .services.open_point_store_search_service import OpenPointStoreSearchService
from .services.family_mart_store_search_service import FamilyMartStoreSearchService
from .services.store_search_reducer import reducer

app = FastAPI()

# add your store search services here
store_search_services = [
    OpenPointStoreSearchService(settings.OPEN_POINT_MID_V),
    FamilyMartStoreSearchService()
]


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

    loc = None
    if location:
        [latitude, longitude] = location.split(",")
        loc = TypeAdapter(GeoLocation).validate_python(
            {"latitude": latitude, "longitude": longitude}
        )

    stores = await reducer(store_search_services, keyword, loc)

    return Response(data=stores)

    # @todo: background. save the stores to the database


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
        stockable_products = await family_mart.get_store_detail(store_id=store_id)

        for sp in stockable_products:
            stocks.append(
                Stock(
                    name=sp.name,
                    quantity=sp.qty,
                    category_id=sp.sub_category_code,
                    category_name=sp.sub_category_name,
                )
            )
    except Exception as e:
        print(e, file=sys.stderr)

    # @todo: background. save the stock information to the database

    return Response(data=stocks)
