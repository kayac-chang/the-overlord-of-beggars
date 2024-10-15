import type { MetaFunction } from "@remix-run/node";
import { useLoaderData } from "@remix-run/react";
import { StoreWithNearExpiredFoodSchema } from "~/models/store_with_near_expired_foods";
import getNearExpiredFoodsByStoreId from "~/services/get_near_expired_foods_by_store_id";
import searchStoresByGeoLocation from "~/services/search_stores_by_geolocation";

export const meta: MetaFunction = () => {
  return [
    { title: "New Remix App" },
    { name: "description", content: "Welcome to Remix!" },
  ];
};

export async function loader() {
  // 透過經緯度搜尋附近的店家
  const stores = await searchStoresByGeoLocation({
    location: {
      latitude: 24.986227,
      longitude: 121.4534552,
    },
  });

  // 取得每家店的即將過期的食物
  return Promise.all(
    stores.map((store) =>
      getNearExpiredFoodsByStoreId(store.id)
        //
        .then((nearExpiredFoods) => ({ ...store, nearExpiredFoods }))
        .then(StoreWithNearExpiredFoodSchema.parseAsync)
    )
  );
}

export default function Index() {
  const data = useLoaderData<typeof loader>();
  console.log(data);
  return (
    <>
      <ul>
        {data.map((store) => (
          <li key={store.id}>
            <div>
              <h3>{store.name}</h3>
              <p>{store.address}</p>
              <ul>
                {store.nearExpiredFoods.map((nearExpiredFood) => (
                  <li key={nearExpiredFood.name}>
                    <p>
                      {nearExpiredFood.name} - {nearExpiredFood.quantity}
                    </p>
                  </li>
                ))}
              </ul>
            </div>
          </li>
        ))}
      </ul>
    </>
  );
}
