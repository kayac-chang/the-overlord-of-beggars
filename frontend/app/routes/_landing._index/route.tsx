import type { MetaFunction } from "@remix-run/node";
import { Form, Link, useLoaderData } from "@remix-run/react";
import StoreTable from "./store_table";
import NearExpiredFoodTable from "./near_expired_food_table";
import { Input } from "~/components/ui/input";
import { Button } from "~/components/ui/button";
import { Toggle } from "~/components/ui/toggle";
import { LocateFixed, Locate, Bookmark } from "lucide-react";
import { clientLoader } from "./client_loader";

export { loader } from "./loader";
export { clientLoader } from "./client_loader";
export { action } from "./action";

export const meta: MetaFunction = () => {
  return [
    { title: "首頁 | The Overload Of Beggars 乞丐超人" },
    //
  ];
};

function LocateToggle() {
  const data = useLoaderData<typeof clientLoader>();
  const pressed = Boolean(data?.query.location);

  if (pressed) {
    return (
      <Toggle
        key="on"
        type="submit"
        className="group w-full h-full rounded-full md:rounded-md"
        defaultPressed={pressed}
      >
        <LocateFixed className="group-data-[state=off]:hidden" />
        <Locate className="group-data-[state=on]:hidden" />
      </Toggle>
    );
  }

  return (
    <Toggle
      key="off"
      type="submit"
      className="group w-full h-full rounded-full md:rounded-md"
      defaultPressed={pressed}
      name="location"
    >
      <Locate className="group-data-[state=on]:animate-blink" />
    </Toggle>
  );
}

export default function Index() {
  const data = useLoaderData<typeof clientLoader>();
  return (
    <div className="max-w-screen-lg mx-auto px-8 pt-8 pb-32 md:pb-8">
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
            <input type="hidden" name="location" value={data.query.location} />
          )}
        </Form>

        <div className="fixed bottom-4 right-4 z-10 flex flex-col gap-4 md:static md:flex-row">
          <Form className="w-12 h-12 md:w-auto md:h-auto">
            <LocateToggle />

            {data?.query.keyword && (
              <input type="hidden" name="keyword" value={data.query.keyword} />
            )}
          </Form>

          <Button
            variant="secondary"
            className="w-12 h-12 rounded-full gap-1 md:w-auto md:h-auto md:rounded-md md:gap-2"
            asChild
          >
            <Link to="/">
              <Bookmark />
              <span className="hidden md:inline">已收藏</span>
              <span>{data?.query.bookmarks.length ?? 0}</span>
            </Link>
          </Button>
        </div>
      </div>

      {/* display the nearby stores and their near expired foods */}
      <StoreTable
        className="mt-4"
        data={data?.stores.filter((store) => store !== null) ?? []}
        expanded={data?.query.stores ?? undefined}
        renderSubComponent={(store) => {
          const found = data?.storesWithNearExpiredFoods?.find(
            (item) => item.storeid === store.id
          );
          return <NearExpiredFoodTable data={found?.nearExpiredFoods ?? []} />;
        }}
      />
    </div>
  );
}
