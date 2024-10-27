import { z } from "zod";
import { match } from "ts-pattern";
import { ClientLoaderFunctionArgs, replace } from "@remix-run/react";
import { coerceToArray, makeSearchParamsObjSchema } from "~/lib/utils";
import Geolocation from "~/models/geolocation";
import { SUPPORT_BRANDS } from "~/models/brand";
import { loader } from "./loader";

const QuerySchema = makeSearchParamsObjSchema(
  z.object({
    location: z.string().nullish(),
    keyword: z.string().nullish(),
    brands: z.array(z.enum(SUPPORT_BRANDS)).nullish(),
    stores: coerceToArray(z.array(z.string())).nullish(),
  })
);

export async function clientLoader(args: ClientLoaderFunctionArgs) {
  const url = new URL(args.request.url);

  const query = await QuerySchema.parseAsync(url.searchParams);

  return match(query)
    .with({ keyword: "" }, () => {
      url.searchParams.delete("keyword");
      return replace(url.toString());
    })
    .with({ stores: [] }, () => {
      url.searchParams.delete("stores");
      return replace(url.toString());
    })
    .with({ location: "" }, () =>
      new Promise<GeolocationPosition>((resolve, reject) =>
        navigator.geolocation.getCurrentPosition(resolve, reject)
      )
        .then((position) => {
          const location = Geolocation.serialize({
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
          });
          url.searchParams.set("location", location);
          return replace(url.toString());
        })
        .catch(() => {
          url.searchParams.delete("location");
          return replace(url.toString());
        })
    )
    .otherwise(args.serverLoader<typeof loader>);
}
clientLoader.hydrate = true;
