import { z } from "zod";
import { GeoLocationSchema } from "~/models/geolocation";
import { Store, StoreSchema } from "~/models/store";
import { ResponseSchema, api } from "./shared";

const InputSchema = z.object({
  // 位置
  location: GeoLocationSchema,
});

type Input = z.infer<typeof InputSchema>;

async function searchStoresByGeoLocation(input: Input): Promise<Store[]> {
  return InputSchema.parseAsync(input)
    .then((input) =>
      [input.location.latitude, input.location.longitude].join(",")
    )
    .then((location) =>
      api.get("stores", { searchParams: { location } }).json()
    )
    .then(ResponseSchema(z.array(StoreSchema)).parseAsync)
    .then(({ data }) => data);
}

export default searchStoresByGeoLocation;
