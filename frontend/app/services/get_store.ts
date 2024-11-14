import { z } from "zod";
import { SUPPORT_BRANDS } from "~/models/brand";
import { Store, StoreSchema } from "~/models/store";
import { api, ResponseSchema } from "./shared";
import {
  GeoLocationSchema,
  toString as toGeoString,
} from "~/models/geolocation";

const InputSchema = z.object({
  storeid: z.string(),
  brand: z.enum(SUPPORT_BRANDS),
  location: GeoLocationSchema.nullish(),
});

type Input = z.infer<typeof InputSchema>;

async function getStore(input: Input, options?: RequestInit): Promise<Store> {
  return InputSchema.parseAsync(input)
    .then(({ brand, storeid, location }) => {
      if (location) {
        const search = new URLSearchParams({ location: toGeoString(location) });

        return api.get(`stores/${brand}/${storeid}?${search}`, options).json();
      }

      return api.get(`stores/${brand}/${storeid}`, options).json();
    })
    .then(ResponseSchema(StoreSchema).parseAsync)
    .then(({ data }) => data);
}
export default getStore;
