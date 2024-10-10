from fastapi import FastAPI, Query

from backend.models.response import Response
from backend.models.stock import Stock
from backend.models.store import Store

app = FastAPI()


@app.get("/stores")
def get_stores(address: str = Query(...)) -> Response[list[Store]]:
    """
    地址查詢門市
    """

    # search the stores from data sources ( 7-11, FamilyMart, ...etc )
    #     -> background. save the stores to the database

    return Response[list[Store]].model_validate(
        {
            "data": [
                {
                    "id": 1,
                    "name": "好市多",
                    "address": "台北市信義區市府路1號",
                    "latitude": 25.034,
                    "longitude": 121.564,
                },
                {
                    "id": 2,
                    "name": "家樂福",
                    "address": "台北市信義區市府路2號",
                    "latitude": 25.035,
                    "longitude": 121.565,
                },
            ]
        }
    )


@app.get("/stores/{store_id}/stock")
def get_store_stock(store_id: str) -> Response[list[Stock]]:
    """
    查詢門市庫存
    """

    # search the stock of the stores from data sources
    #     -> background. save the stock information to the database

    return Response[list[Stock]].model_validate(
        {
            "data": [
                {
                    "id": 1,
                    "name": "肥皂",
                    "quantity": 100,
                },
                {
                    "id": 2,
                    "name": "洗髮精",
                    "quantity": 200,
                },
            ]
        }
    )
