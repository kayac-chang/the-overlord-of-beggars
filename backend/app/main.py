import asyncio
from typing import Annotated

from fastapi import Depends, FastAPI, Path, Query
from fastapi.exceptions import HTTPException
from pydantic import TypeAdapter

from app.services.stock_search_service import StockSearchService

from .config import settings
from .models.brand import Brand
from .models.geolocation import GeoLocation
from .models.response import Response
from .models.stock import Stock
from .models.store import Store
from .services.store_search_service import StoreSearchService

app = FastAPI()


def parse_location(
    location: Annotated[
        str | None,
        Query(
            description="經緯度座標",
            pattern=r"^-?\d+\.\d+,-?\d+\.\d+$",
        ),
    ] = None
) -> GeoLocation | None:
    if not location:
        return None

    [latitude, longitude] = location.split(",")
    return TypeAdapter(GeoLocation).validate_python(
        {"latitude": latitude, "longitude": longitude}
    )


Location = Annotated[GeoLocation | None, Depends(parse_location)]
StoreId = Annotated[str, Path(description="店號")]
Keyword = Annotated[str | None, Query(description="關鍵字")]
Brands = Annotated[set[Brand] | None, Query(description="品牌(多選)")]
Brand = Annotated[Brand, Path(description="品牌")]


store_search_service = StoreSearchService(
    openai_api_key=settings.OPENAI_API_KEY,
    db_url=settings.NEON_DB_URL,
)

stock_search_service = StockSearchService(
    open_point_mid_v=settings.OPEN_POINT_MID_V,
)


@app.get("/stores")
async def get_stores(
    keyword: Keyword = None,
    brands: Brands = None,
    location: Location = None,
) -> Response[list[Store]]:
    """
    查詢門市
    """
    stores: list[Store] = []
    match (keyword, location):
        # 提供關鍵字與地理位置，搜尋接近關鍵字的店家，並提供距離。
        case (
            str() as keyword,
            {"latitude": float(), "longitude": float()} as location,
        ):
            stores = await store_search_service.get_stores_by_keyword_and_location(
                keyword=keyword, location=location, brands=brands
            )

        # 提供關鍵字，搜尋接近關鍵字的店家。
        case (str() as keyword, None):
            stores = await store_search_service.get_stores_by_keyword(
                keyword=keyword, brands=brands
            )

        # 提供當前地理位置，搜尋周遭的店家。
        case (None, {"latitude": float(), "longitude": float()} as location):
            stores = await store_search_service.get_stores_by_location(
                location=location, brands=brands
            )

        case _:
            raise HTTPException(status_code=400, detail="Invalid query parameters")

    # 查詢每家店是否有即期品
    tasks = [
        stock_search_service.has_stocks_in_store(store_id=store.id, brand=store.brand)
        for store in stores
    ]
    has_stocks = await asyncio.gather(*tasks)
    res = [store for store, has_stock in zip(stores, has_stocks) if has_stock]

    return Response(data=res)


@app.get("/stores/{brand}/{store_id}")
async def get_store(
    store_id: StoreId, brand: Brand, location: Location = None
) -> Response[Store | None]:
    """
    店號查詢門市
    """
    store: Store | None = None

    if location:
        store = await store_search_service.get_store_by_store_id_and_location(
            id=store_id, location=location, brand=brand
        )
    else:
        store = await store_search_service.get_store_by_store_id(
            id=store_id, brand=brand
        )

    if not store:
        raise HTTPException(status_code=404, detail="Store not exist")

    return Response(data=store)


@app.get("/stores/{brand}/{store_id}/stock")
async def get_store_stock(store_id: StoreId, brand: Brand) -> Response[list[Stock]]:
    """
    查詢門市庫存
    """
    # 檢查門市是否存在
    store = await store_search_service.get_store_by_store_id(id=store_id, brand=brand)

    if not store:
        raise HTTPException(status_code=404, detail="Store not exist")

    stocks = await stock_search_service.get_stocks_in_store(
        store_id=store_id, brand=brand
    )

    return Response(data=stocks)
