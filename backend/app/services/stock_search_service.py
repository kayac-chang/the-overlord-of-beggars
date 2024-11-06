from app.data_sources import family_mart, open_point
from app.models.brand import Brand
from app.models.stock import Stock


class StockSearchService:
    def __init__(self, open_point_mid_v: str):
        self.open_point_mid_v = open_point_mid_v

    async def has_stocks_in_store(self, store_id: str, brand: Brand) -> bool:
        stocks = await self.get_stocks_in_store(store_id=store_id, brand=brand)

        return bool(stocks)

    async def get_stocks_in_store(self, store_id: str, brand: Brand) -> list[Stock]:

        match brand:
            case "7-11":
                # get access token for open point
                token = await open_point.get_access_token(self.open_point_mid_v)

                # search the stock of the stores from data sources
                detail = await open_point.get_store_detail(
                    token=token, store_id=store_id
                )

                if not detail:
                    return []

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

                return stocks

            case "FamilyMart":
                # search the stock of the stores from data sources
                store = await family_mart.get_store_detail(store_id=store_id)

                if not store:
                    return []

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

                return stocks
