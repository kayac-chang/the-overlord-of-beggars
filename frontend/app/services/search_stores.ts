import { z } from "zod";
import {
  GeoLocationSchema,
  toString as toGeoString,
} from "~/models/geolocation";
import { Store, StoreSchema } from "~/models/store";
import { ResponseSchema, api } from "./shared";
import { SUPPORT_BRANDS } from "~/models/brand";

const InputSchema = z.object({
  keyword: z.string().nullish(),
  location: GeoLocationSchema.nullish(),
  brands: z.array(z.enum(SUPPORT_BRANDS)).nullish(),
});

type Input = z.infer<typeof InputSchema>;

async function searchStores(input: Input): Promise<Store[]> {
  return InputSchema.parseAsync(input)
    .then((input) => {
      const searchParams = new URLSearchParams();
      if (input.keyword) {
        searchParams.append("keyword", input.keyword);
      }
      if (input.location) {
        searchParams.append("location", toGeoString(input.location));
      }
      if (input.brands) {
        input.brands.forEach((brand) => searchParams.append("brands", brand));
      }
      return searchParams;
    })
    .then((searchParams) => api.get("stores", { searchParams }).json())
    .then(ResponseSchema(z.array(StoreSchema)).parseAsync)
    .then(({ data }) => data);
}
export default searchStores;
