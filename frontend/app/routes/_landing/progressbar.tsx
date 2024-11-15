import { useNavigation } from "@remix-run/react";
import { cn } from "~/lib/utils";
import { useEffect, useState } from "react";
import { match } from "ts-pattern";

export default function Progressbar() {
  const navigation = useNavigation();
  const [previous, setPrevious] = useState(navigation.state);
  const loading = navigation.state === "loading";

  useEffect(() => {
    setPrevious(navigation.state);
  }, [navigation.state]);

  return (
    <div
      role="progressbar"
      aria-hidden={loading ? "true" : "false"}
      aria-label="載入中"
      className="fixed inset-x-0 left-0 top-0 z-50 h-1 animate-pulse"
    >
      <div
        className={cn(
          "h-full",
          "bg-gradient-to-r from-indigo-500 via-indigo-400 to-transparent",
          "transition-all duration-500 ease-in-out",

          match({ current: navigation.state, previous })
            .with({ current: "loading" }, () => "w-10/12")
            .with({ current: "idle", previous: "loading" }, () => "w-full")
            .otherwise(() => "w-0 opacity-0 transition-none")
        )}
      />
    </div>
  );
}
