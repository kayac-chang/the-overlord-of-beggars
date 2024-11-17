import { ComponentProps, ReactNode } from "react";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "~/components/ui/card";
import { Separator } from "~/components/ui/separator";
import { Badge } from "~/components/ui/badge";
import { BookmarkButton } from "./bookmark";
import { Store } from "~/models/store";
import {
  Drawer,
  DrawerContent,
  DrawerDescription,
  DrawerHeader,
  DrawerTitle,
} from "~/components/ui/drawer";
import { Form, useLoaderData, useSearchParams } from "@remix-run/react";
import { clientLoader } from "./client_loader";
import useMedia from "~/lib/use_media";

type StoreListProps = ComponentProps<"div"> & {
  data: Store[];
  expanded?: Store["id"][];
  renderSubComponent?: (data: Store) => ReactNode;
};
function StoreList({
  renderSubComponent,
  data,
  expanded,
  ...props
}: StoreListProps) {
  const _data = useLoaderData<typeof clientLoader>();

  const [searchParams, setSearchParams] = useSearchParams();
  function onClose() {
    if (searchParams.has("stores")) {
      searchParams.delete("stores");
      setSearchParams(searchParams, {
        preventScrollReset: true,
      });
    }
  }

  const isMd = useMedia("(max-width: 768px)", true);

  const stores = data
    .filter((store) => store !== null)
    .map((store) => (
      <li key={store.id}>
        <Card className="relative">
          {store.distance && (
            <Badge className="absolute end-0 -translate-y-3 -translate-x-2">
              {Intl.NumberFormat("zh-TW", {
                style: "unit",
                unit: "meter",
                maximumFractionDigits: 0,
              }).format(store.distance)}
            </Badge>
          )}

          <CardHeader>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2 h-5">
                <div>店名</div>
                <Separator orientation="vertical" />
                <CardTitle>{store.name}</CardTitle>
              </div>
              <BookmarkButton {...store} />
            </div>
            <Separator />
          </CardHeader>
          <CardContent>
            <ul className="grid gap-3">
              <li>
                <div className="flex items-center gap-2 h-5">
                  <div>廠商</div>
                  <Separator orientation="vertical" />
                  <div>{store.brand}</div>
                </div>
              </li>
              <li>
                <div className="flex items-center gap-2 h-5">
                  <div>地址</div>
                  <Separator orientation="vertical" />
                  <div>{store.address}</div>
                </div>
              </li>
            </ul>
          </CardContent>
          <CardFooter>
            <Form preventScrollReset className="w-full">
              <button type="submit" className="group w-full">
                即期商品資訊 👇
              </button>

              {_data?.query.location && (
                <input
                  type="hidden"
                  name="location"
                  value={_data.query.location}
                />
              )}
              {_data?.query.keyword && (
                <input
                  type="hidden"
                  name="keyword"
                  value={_data.query.keyword}
                />
              )}
              <input type="hidden" name="stores" value={store.id} />
            </Form>

            <Drawer
              open={expanded?.includes(store.id) && isMd}
              onClose={onClose}
            >
              <DrawerContent>
                <DrawerHeader>
                  <DrawerTitle>{store.name}</DrawerTitle>
                </DrawerHeader>

                <div className="px-8 pb-8">
                  <DrawerDescription>即期商品資訊</DrawerDescription>
                  <div className="max-h-[50vh] overflow-auto mt-4">
                    {renderSubComponent?.(store)}
                  </div>
                </div>
              </DrawerContent>
            </Drawer>
          </CardFooter>
        </Card>
      </li>
    ));

  return (
    <div {...props}>
      <ul className="grid gap-8">{stores}</ul>
    </div>
  );
}

export default StoreList;
