import { Form, useLoaderData } from "@remix-run/react";
import { clientLoader } from "./client_loader";
import { LoaderCircle } from "lucide-react";
import { Toggle } from "~/components/ui/toggle";
import { cn } from "~/lib/utils";

type ExpandButtonProps = {
  value: string;
  pressed?: boolean;
  onPressedChange?: () => void;
  children?: React.ReactNode;
  formClassName?: string;
  className?: string;
};
function ExpandButton(props: ExpandButtonProps) {
  const data = useLoaderData<typeof clientLoader>();
  const hasLoaded = Boolean(data?.storesWithNearExpiredFoods);

  // 展開點下去瞬間 icon 要變成 loading
  if (props.pressed && hasLoaded) {
    return (
      <Form preventScrollReset className={props.formClassName}>
        <Toggle
          type="submit"
          defaultPressed={props.pressed}
          onPressedChange={props.onPressedChange}
          className={cn("group", props.className)}
        >
          {props.children}
          <span className="group-data-[state=off]:hidden">👇</span>
          <span className="group-data-[state=on]:hidden">
            <LoaderCircle className="size-4 animate-spin" />
          </span>
        </Toggle>

        {data?.query.location && (
          <input type="hidden" name="location" value={data.query.location} />
        )}
        {data?.query.keyword && (
          <input type="hidden" name="keyword" value={data.query.keyword} />
        )}
        {data?.query.stores &&
          data.query.stores
            .filter((store) => store !== props.value)
            .map((store) => (
              <input key={store} type="hidden" name="stores" value={store} />
            ))}
      </Form>
    );
  }

  return (
    <Form preventScrollReset className={props.formClassName}>
      <Toggle
        type="submit"
        defaultPressed={props.pressed}
        onPressedChange={props.onPressedChange}
        name="stores"
        value={props.value}
        className={cn("group", props.className)}
      >
        {props.children}
        <span className="group-data-[state=on]:hidden">👉</span>
        <span className="group-data-[state=off]:hidden">
          <LoaderCircle className="size-4 animate-spin" />
        </span>
      </Toggle>

      {data?.query.location && (
        <input type="hidden" name="location" value={data.query.location} />
      )}
      {data?.query.keyword && (
        <input type="hidden" name="keyword" value={data.query.keyword} />
      )}
      {data?.query.stores &&
        data.query.stores
          .filter((store) => store !== props.value)
          .map((store) => (
            <input key={store} type="hidden" name="stores" value={store} />
          ))}
    </Form>
  );
}

export default ExpandButton;
