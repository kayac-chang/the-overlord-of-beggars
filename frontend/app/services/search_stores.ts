import { z } from "zod";
import {
  GeoLocationSchema,
  toString as toGeoString,
} from "~/models/geolocation";
import { Store, StoreSchema } from "~/models/store";
import { ResponseSchema, api } from "./shared";
import { P, match } from "ts-pattern";

const InputSchema = z.object({
  keyword: z.string().nullish(),
  location: GeoLocationSchema.nullish(),
});

type Input = z.infer<typeof InputSchema>;

async function searchStores(input: Input): Promise<Store[]> {
  return InputSchema.parseAsync(input)
    .then((input) =>
      match(input)
        .with({ keyword: P.nonNullable, location: P.nonNullable }, (input) => ({
          keyword: input.keyword,
          location: toGeoString(input.location),
        }))
        .with({ keyword: P.nonNullable }, (input) => ({
          keyword: input.keyword,
        }))
        .with({ location: P.nonNullable }, (input) => ({
          location: toGeoString(input.location),
        }))
        .otherwise(() => {
          throw new Error("Invalid input");
        })
    )
    .then((searchParams) => api.get("stores", { searchParams }).json())
    .then(ResponseSchema(z.array(StoreSchema)).parseAsync)
    .then(({ data }) => data);
}

export default searchStores;
