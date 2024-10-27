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
        key={pressed ? "on" : "off"}
        type="submit"
        className="group"
        defaultPressed={pressed}
      >
        <LocateFixed className="group-data-[state=off]:hidden" />
        <Locate className="group-data-[state=on]:hidden" />
      </Toggle>
    );
  }

  return (
    <Toggle
      key={pressed ? "on" : "off"}
      type="submit"
      className="group"
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
    <div className="max-w-screen-lg mx-auto px-8 py-8">
      <div className="flex gap-4">
        <Form className="flex gap-4 flex-1">
          <Input
            type="search"
            name="keyword"
            defaultValue={data?.query.keyword ?? ""}
            placeholder="搜尋地址"
            autoComplete="off"
          />

          <Button type="submit">送出</Button>

          {data?.query.location && (
            <input type="hidden" name="location" value={data.query.location} />
          )}
        </Form>

        <Form>
          <LocateToggle />

          {data?.query.keyword && (
            <input type="hidden" name="keyword" value={data.query.keyword} />
          )}
        </Form>

        <Button variant="secondary" asChild>
          <Link to="/">
            <Bookmark />
            <span>已收藏 {data?.query.bookmarks.length ?? 0}</span>
          </Link>
        </Button>
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
