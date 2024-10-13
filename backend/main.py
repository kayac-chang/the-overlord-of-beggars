from fastapi import FastAPI, Query

from backend.config import settings
from backend.data_sources.open_point.get_access_token import get_access_token
from backend.data_sources.open_point.get_store_detail import get_store_detail
from backend.data_sources.open_point.get_stores_by_address import get_stores_by_address
from backend.models.response import Response
from backend.models.stock import Stock
from backend.models.store import Store

app = FastAPI()


@app.get("/stores")
async def get_stores(address: str = Query(...)) -> Response[list[Store]]:
    """
    地址查詢門市
    """

    # get access token for open point
    token = await get_access_token(settings.OPEN_POINT_MID_V)

    # search the stores from data sources ( 7-11, FamilyMart, ...etc )
    _stores = await get_stores_by_address(token=token, keyword=address)
    stores = [
        Store(
            id=store.store_no,
            name=store.store_name,
            address=store.address,
            latitude=store.latitude,
            longitude=store.longitude,
        )
        for store in _stores
    ]

    # @todo: background. save the stores to the database

    return Response(data=stores)


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
