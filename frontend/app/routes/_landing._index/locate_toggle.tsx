import { useLoaderData } from "@remix-run/react";
import { Toggle } from "~/components/ui/toggle";
import { LocateFixed, Locate } from "lucide-react";
import { clientLoader } from "./client_loader";

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
export default LocateToggle;
