import { z } from "zod";
import pProps from "p-props";
import { match, P } from "ts-pattern";
import { LoaderFunctionArgs } from "@remix-run/node";
import getStore from "~/services/get_store";
import getNearExpiredFoodsByStoreId from "~/services/get_near_expired_foods_by_store_id";
import searchStores from "~/services/search_stores";
import { SUPPORT_BRANDS } from "~/models/brand";
import GeoLocation from "~/models/geolocation";
import { coerceToArray, makeSearchParamsObjSchema } from "~/lib/utils";
import BookieCookie from "./cookie";

const QuerySchema = makeSearchParamsObjSchema(
  z.object({
    location: z.string().nullish(),
    keyword: z.string().nullish(),
    brands: z.array(z.enum(SUPPORT_BRANDS)).nullish(),
    stores: coerceToArray(z.array(z.string())).nullish(),
  })
);

export async function loader(args: LoaderFunctionArgs) {
  const [query, bookmarks] = await Promise.all([
    // parse query
    QuerySchema.parseAsync(new URL(args.request.url).searchParams),

    // get bookmarks from cookie
    BookieCookie.deserialize(args.request),
  ]);

  return (
    match({ ...query, bookmarks })
      // 關鍵字 + 經緯度 搜尋附近的店家
      // 關鍵字 搜尋附近的店
      // 經緯度 搜尋附近的店家
      .with(
        P.union(
          {
            keyword: P.string.minLength(1),
            location: P.string.regex(/^\d+\.\d+,\d+\.\d+$/),
          },
          {
            keyword: P.string.minLength(1),
          },
          {
            location: P.string.regex(/^\d+\.\d+,\d+\.\d+$/),
          }
        ),
        (query) =>
          searchStores({
            keyword: query.keyword,
            location: query.location
              ? GeoLocation.deserialize(query.location)
              : undefined,
            brands: query.brands,
          })
            //
            .then((stores) =>
              pProps({
                query,
                stores,
                storesWithNearExpiredFoods: Promise.all(
                  stores
                    .filter((store) => query.stores?.includes(store.id))
                    .map((store) => ({ storeid: store.id, brand: store.brand }))
                    .map((store) =>
                      getNearExpiredFoodsByStoreId(store).then(
                        (nearExpiredFoods) => ({
                          ...store,
                          nearExpiredFoods,
                        })
                      )
                    )
                ),
              })
            )
      )
      // 還未執行任何搜尋
      // 但有關注的店家
      .with(
        {
          bookmarks: [P.any, ...P.array()],
        },
        (query) =>
          pProps({
            query,
            stores: Promise.all(query.bookmarks.map(getStore)).catch(() => []),
            storesWithNearExpiredFoods: Promise.all(
              query.bookmarks
                // only get near expired foods from stores that are bookmarked
                .filter((bookmark) => query.stores?.includes(bookmark.storeid))
                .map((bookmark) =>
                  getNearExpiredFoodsByStoreId(bookmark).then(
                    (nearExpiredFoods) => ({
                      storeid: bookmark.storeid,
                      nearExpiredFoods,
                    })
                  )
                )
            ),
          })
      )
      .otherwise(() => null)
  );
}
