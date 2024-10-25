import aiohttp
import itertools

from .model import Response, Store, ProductWithSubCategory
from .share import PROJECT_CODE

from pprint import pprint

def flatten(list_of_lists):
    return list(itertools.chain.from_iterable(list_of_lists))

async def get_store_detail(
    store_id: str,
) -> list[ProductWithSubCategory]:
    """
    get store detail 取得門市庫存

    POST https://stamp.family.com.tw/api/maps/MapProductInfo
    """

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"https://stamp.family.com.tw/api/maps/MapProductInfo",
             json={
                "ProjectCode": PROJECT_CODE,
                "OldPKeys": [store_id],
            },
        ) as response:

            response_json = await response.json()

            res = Response[list[Store]].model_validate(response_json)

            item_categories = flatten(map(lambda s: s.info ,res.data))

            sub_categories = flatten(map(lambda c: c.categories, item_categories))

            products: list[ProductWithSubCategory] = []
            for sub_category in sub_categories:
                for product in sub_category.products:
                    products.append(ProductWithSubCategory(
                        code=product.code,
                        name=product.name,
                        qty=product.qty,
                        sub_category_code=sub_category.code,
                        sub_category_name=sub_category.name
                    ))

            return products

# python -m app.data_sources.family_mart.get_store_detail
if __name__ == '__main__':
    import asyncio
    from pprint import pprint


    async def main():
        stockableProducts = await get_store_detail('017248')
        pprint(stockableProducts)

    asyncio.run(main())
