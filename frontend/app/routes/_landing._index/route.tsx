import type { LoaderFunctionArgs, MetaFunction } from "@remix-run/node";
import {
  ClientLoaderFunctionArgs,
  redirect,
  useLoaderData,
} from "@remix-run/react";
import { StoreWithNearExpiredFoodSchema } from "~/models/store_with_near_expired_foods";
import getNearExpiredFoodsByStoreId from "~/services/get_near_expired_foods_by_store_id";
import searchStoresByGeoLocation from "~/services/search_stores_by_geolocation";
import StoreTable from "./store_table";
import NearExpiredFoodTable from "./near_expired_food_table";

export const meta: MetaFunction = () => {
  return [
    { title: "首頁 | The Overload Of Beggars 乞丐超人" },
    //
  ];
};

export async function loader({ request }: LoaderFunctionArgs) {
  const url = new URL(request.url);

  const location = url.searchParams.get("location");

  // if the location is not provided, we'll just display the default page
  if (!location) {
    return null;
  }

  // @todo: regex to validate geolocation
  const [latitude, longitude] = location.split(",").map(Number);

  // 透過經緯度搜尋附近的店家
  const stores = await searchStoresByGeoLocation({
    location: { latitude, longitude },
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

export function clientLoader({
  request,
  serverLoader,
}: ClientLoaderFunctionArgs) {
  const url = new URL(request.url);

  // if the location is already provided in the URL, we'll just load the data from the server
  if (url.searchParams.has("location")) {
    return serverLoader<typeof loader>();
  }

  return (
    new Promise<GeolocationPosition>((resolve, reject) =>
      navigator.geolocation.getCurrentPosition(resolve, reject)
    )
      // if user grants location permission, we'll redirect to the page with the location
      .then((position) =>
        redirect(
          "?" +
            new URLSearchParams({
              location: `${position.coords.latitude},${position.coords.longitude}`,
            }).toString()
        )
      )
      // otherwise. user denies location permission, we'll just show the default page
      .catch(() => null)
  );
}
clientLoader.hydrate = true;

export default function Index() {
  const data = useLoaderData<typeof loader>();

  // when the user denies location permission
  // the default page will be rendered
  if (!data) return null;

  // display the nearby stores and their near expired foods
  return (
    <div className="container mx-auto">
      <StoreTable
        className="max-w-screen-lg mx-auto"
        data={data}
        renderSubComponent={(store) => (
          <NearExpiredFoodTable data={store.nearExpiredFoods} />
        )}
      />
    </div>
  );
}
