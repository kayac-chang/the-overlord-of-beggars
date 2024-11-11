import type { MetaFunction } from "@remix-run/node";
import { Form, useLoaderData } from "@remix-run/react";
import { Input } from "~/components/ui/input";
import { Button } from "~/components/ui/button";
import { clientLoader } from "./client_loader";
import StoreTable from "./store_table";
import NearExpiredFoodTable from "./near_expired_food_table";
import { BookmarkProvider, HasBookmarkedButton } from "./bookmark";
import LocateToggle from "./locate_toggle";

export { loader } from "./loader";
export { clientLoader } from "./client_loader";
export { action } from "./action";

export const meta: MetaFunction = () => {
  return [
    { title: "首頁 | The Overload Of Beggars 乞丐超人" },
    //
  ];
};

export default function Index() {
  const data = useLoaderData<typeof clientLoader>();
  return (
    <BookmarkProvider>
      <div className="max-w-screen-lg mx-auto px-4 md:px-8 pt-4 md:pt-8 pb-32 md:pb-8">
        <div className="flex gap-4">
          <Form className="flex gap-4 flex-1">
            <Input
              type="search"
              name="keyword"
              defaultValue={data?.query.keyword ?? ""}
              placeholder="搜尋 店名 / 地址"
              autoComplete="off"
            />

            <Button type="submit">送出</Button>

            {data?.query.location && (
              <input
                type="hidden"
                name="location"
                value={data.query.location}
              />
            )}
          </Form>

          <div className="fixed bottom-4 right-4 z-10 flex flex-col gap-4 md:static md:flex-row">
            <Form className="w-12 h-12 md:w-auto md:h-auto">
              <LocateToggle />

              {data?.query.keyword && (
                <input
                  type="hidden"
                  name="keyword"
                  value={data.query.keyword}
                />
              )}
            </Form>

            <HasBookmarkedButton />
          </div>
        </div>

        {/* display the nearby stores and their near expired foods */}
        <StoreTable
          className="mt-8"
          data={data?.stores.filter((store) => store !== null) ?? []}
          expanded={data?.query.stores ?? undefined}
          renderSubComponent={(store) => {
            const found = data?.storesWithNearExpiredFoods?.find(
              (item) => item.storeid === store.id
            );
            return (
              <NearExpiredFoodTable data={found?.nearExpiredFoods ?? []} />
            );
          }}
        />
      </div>
    </BookmarkProvider>
  );
}
