from typing import Annotated

from fastapi import FastAPI, Path, Query
from fastapi.exceptions import HTTPException
from pydantic import TypeAdapter

from .config import settings
from .data_sources import family_mart
from .data_sources.open_point.get_access_token import get_access_token
from .data_sources.open_point.get_store_detail import get_store_detail
from .models.brand import Brand
from .models.geolocation import GeoLocation
from .models.response import Response
from .models.stock import Stock
from .models.store import Store
from .services.family_mart_store_search_service import FamilyMartStoreSearchService
from .services.open_point_store_search_service import OpenPointStoreSearchService
from .services.store_search_reducer import reducer
from .services.store_search_service import StoreSearchService

app = FastAPI()

# store search services
store_search_services: dict[Brand, StoreSearchService] = {
    "7-11": OpenPointStoreSearchService(settings.OPEN_POINT_MID_V),
    "FamilyMart": FamilyMartStoreSearchService(),
}

# list of parameters
Location = Annotated[
    str | None,
    Query(description="經緯度座標", regex=r"^-?\d+\.\d+,-?\d+\.\d+$"),
]
StoreId = Annotated[str, Path(description="店號")]
Keyword = Annotated[str | None, Query(description="關鍵字")]
Brands = Annotated[set[Brand] | None, Query(description="品牌(多選)")]
Brand = Annotated[Brand, Path(description="品牌")]


@app.get("/stores")
async def get_stores(
    location: Location = None, keyword: Keyword = None, brands: Brands = None
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

    services = [
        service
        for brand, service in store_search_services.items()
        if not brands or brand in brands
    ]

    stores = await reducer(services, keyword, loc)

    return Response(data=stores)


@app.get("/stores/{brand}/{store_id}")
async def get_store(
    store_id: StoreId, brand: Brand, location: Location = None
) -> Response[Store]:
    """
    店號查詢門市
    """

    loc = None
    if location:
        [latitude, longitude] = location.split(",")
        loc = TypeAdapter(GeoLocation).validate_python(
            {"latitude": latitude, "longitude": longitude}
        )

    # get the store search service by brand
    service = store_search_services.get(brand)

    # throw 404 if the brand not exist
    if not service:
        raise HTTPException(status_code=404, detail="Brand not exist")

    # search the store by store id from data sources
    if loc:
        store = await service.get_store_by_store_id_and_location(
            id=store_id, location=loc
        )
    else:
        store = await service.get_store_by_store_id(id=store_id)

    # throw 404 if the store not exist
    if not store:
        raise HTTPException(status_code=404, detail="Store not exist")

    return Response(data=store)


@app.get("/stores/{brand}/{store_id}/stock")
async def get_store_stock(store_id: StoreId, brand: Brand) -> Response[list[Stock]]:
    """
    查詢門市庫存
    """

    match brand:
        case "7-11":
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

            return Response(data=stocks)

        case "FamilyMart":
            # search the stock of the stores from data sources
            store = await family_mart.get_store_detail(store_id=store_id)

            # throw 404 if the store not exist
            if not store:
                raise HTTPException(status_code=404, detail="Store not exist")

            stocks = []
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

            return Response(data=stocks)

        case _:
            raise HTTPException(status_code=404, detail="Brand not exist")
